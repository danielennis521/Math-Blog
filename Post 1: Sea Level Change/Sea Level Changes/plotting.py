import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from math import ceil


def build_plots():
    # ----------------
    # MONTHLY SEA LEVEL
    # ----------------
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
        monthly_sea_level = df.resample('ME').mean()
        #monthly_sea_level.drop('2025-12-31', inplace=True)

        monthly_sea_level = monthly_sea_level[monthly_sea_level.index > pd.Timestamp('1970-01-01')]
        sea_level_data[file[:-4]] = monthly_sea_level


    n = ceil(len(sea_level_data)/2)

    fig, ax = plt.subplots(2, n)
    fig.suptitle('US East Coast Sea Levels')
    fig.supylabel('Sea Level')
    fig.supxlabel('Month')

    i=0
    for location, df in sea_level_data.items():
        ax[i//n][i%n].plot(df)
        ax[i//n][i%n].set_title(location)
        ax[i//n][i%n].tick_params(axis='x', labelrotation=45)
        i+=1

    fig.tight_layout()
    plt.show()


    # --------------------------
    # FILTERED YEARLY SEA LEVEL
    # --------------------------
    data_files = os.listdir('.\\Processed Data\\')
    sea_level_data = {}

    fig, ax = plt.subplots(2, n)
    fig.suptitle('Filtered US East Coast Sea Levels')
    fig.supylabel('Sea Level')
    fig.supxlabel('Year')

    i=0
    for file in data_files:
        df = pd.read_csv(f'.\\Processed Data\\{file}')
        df['date'] = pd.to_datetime(df['date'])
        sea_level_data[file[:-4]] = df.set_index('date')

        ax[i//n][i%n].plot(df.set_index('date'))
        ax[i//n][i%n].set_title(file[:-4])
        ax[i//n][i%n].tick_params(axis='x', labelrotation=45)
        i+=1

    fig.tight_layout()
    plt.show()


    # -----------------------
    # DERIVATIVE BASED PLOTS
    # -----------------------
    deriv_fits = pd.read_csv('.\\Results\\derivative regression.csv')
    deriv_fits.set_index('Dataset', inplace=True)
    fig, ax = plt.subplots(2, n)
    fig.suptitle('Linear Regression on First Derivatives')
    fig.supylabel('Sea Level Change (Year over Year)')
    fig.supxlabel('Start Year')

    i=0
    for location, df in sea_level_data.items():
        changes = df['sea level'].diff().dropna()
        m = len(changes)
        beta0, beta1, CI = deriv_fits.loc[location]

        x = np.arange(m)
        y = changes.to_numpy()
        z = beta0 + beta1*x

        ax[i//n][i%n].plot(df[:-1].index, y)
        ax[i//n][i%n].plot(df[:-1].index, z)
        ax[i//n][i%n].set_title(location[:-7])
        ax[i//n][i%n].tick_params(axis='x', labelrotation=45)
        i+=1

    fig.tight_layout()
    plt.show()


    # ---------------------------
    # QUADRATIC REGRESSION PLOTS
    # ---------------------------
    quadratic_fits = pd.read_csv('.\\Results\\quadratic regression.csv')
    quadratic_fits.set_index('Dataset', inplace=True)
    fig, ax = plt.subplots(2, n)
    fig.suptitle('Quadratic Regression of Sea Level')
    fig.supylabel('Sea Level')
    fig.supxlabel('Year')

    i=0
    for location, df in sea_level_data.items():
        m = len(df)
        beta0, beta1, beta2, CI = quadratic_fits.loc[location]

        x = np.arange(m)
        y = df['sea level'].to_numpy()
        z = beta0 + beta1*x + beta2*x**2

        ax[i//n][i%n].plot(df.index, y)
        ax[i//n][i%n].plot(df.index, z)
        ax[i//n][i%n].set_title(location[:-7])
        ax[i//n][i%n].tick_params(axis='x', labelrotation=45)
        i+=1

    fig.tight_layout()
    plt.show()


    # -------------------------
    # RATE OF CHANGE ESTIMATES
    # -------------------------
    fig, ax = plt.subplots(2, n)
    fig.suptitle('Rate of Change Estimates')
    fig.supylabel('Sea Level Increase Per Year')
    fig.supxlabel('Year')
    i=0
    for location in sea_level_data.keys():
        df = pd.read_csv(f'.\\Results\\{location[:4]} - rate of change.csv')
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        ax[i//n][i%n].plot(df.index, df['rate'], label='rate', color='b')
        ax[i//n][i%n].plot(df.index, df['lower bound'], label='95% CI', color='k', linestyle='dashed')
        ax[i//n][i%n].plot(df.index, df['upper bound'], color='k', linestyle='dashed')

        ax[i//n][i%n].legend()
        ax[i//n][i%n].tick_params(axis='x', labelrotation=45)
        ax[i//n][i%n].set_title(location[:-7])
        i+=1

    fig.tight_layout()
    plt.show()