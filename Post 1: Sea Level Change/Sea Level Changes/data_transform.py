import pandas as pd
from numpy import arange, abs
from scipy.stats import zscore
from sklearn import linear_model as lm
import os


def transform():
        
    pd.set_option('future.no_silent_downcasting', True)

    data_files = os.listdir('.\\Raw Data\\')
    sea_level_data = {}

    for file in data_files:
        # read file and adjust formatting
        df = pd.read_csv(f'.\\Raw Data\\{file}', header=None)
        df.rename(columns={0:'year', 1:'month', 2:'day', 3:'sea level'}, inplace=True)
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        df.drop(['year', 'month', 'day'], axis=1, inplace=True)
        df.set_index('date',inplace=True)


        # fill missing data and aggregate to monthly
        df.replace(-32767, None, inplace=True)
        df['sea level'] = df['sea level'].ffill()
        yearly_sea_level = df.resample('YE').mean()
        yearly_sea_level.drop('2025-12-31', inplace=True)

        # compute trend of sea level data
        n = len(yearly_sea_level['sea level'])
        y = yearly_sea_level['sea level'].to_numpy()
        x = arange(n).reshape(-1, 1)
        y = y.reshape(-1, 1)

        reg = lm.LinearRegression()
        reg.fit(x,y)

        trend = reg.intercept_[0] + reg.coef_[0]*arange(n)
        yearly_sea_level['adjusted level'] = yearly_sea_level['sea level'] - trend
        
        
        # filter outliers based on z-scores of trend corrected data
        yearly_sea_level['zscore'] = zscore(yearly_sea_level['adjusted level'].astype(float))
        yearly_sea_level.loc[abs(yearly_sea_level['zscore']) >= 3.5, 'sea level'] = None
        yearly_sea_level['sea level'] = yearly_sea_level['sea level'].ffill()


        # 
        yearly_sea_level.drop(['adjusted level', 'zscore'], axis=1, inplace=True)
        yearly_sea_level = yearly_sea_level[yearly_sea_level.index > pd.Timestamp('1970-01-01')]
        yearly_sea_level.to_csv(f'.\\Processed Data\\{file[:-4]}-yearly.csv')
