import pandas as pd
import numpy as np
from math import sqrt
from scipy.stats import  t, f
from sklearn import linear_model as lm
import os


def regression_analysis():
        
    data_files = os.listdir('.\\Processed Data\\')
    sea_level_data = {}

    deriv_reg_results = pd.DataFrame(columns=['Dataset', 'beta0', 'beta1', 'beta1 CI'])
    quadratic_results = pd.DataFrame(columns=['Dataset', 'beta0', 'beta1', 'beta2', 'beta1 C2'])

    for file in data_files:
        # read file and adjust formatting
        df = pd.read_csv(f'.\\Processed Data\\{file}')
        reg = lm.LinearRegression()

        # -------------------------------
        # LINEAR REGRESSION ON DERIVATIVE
        # -------------------------------

        # get year-over-year changes
        changes = df['sea level'].diff().dropna()
        n = len(changes)

        # construct independent variables
        x = np.arange(n).reshape(-1, 1)
        y = changes.to_numpy().reshape(-1, 1)

        # fit regression
        reg.fit(x, y)
        y_hat = reg.predict(x)

        # compute residuals and standard error
        residuals = y - y_hat
        s_squared = (residuals**2).sum() / (n - 2)
        s = sqrt(s_squared)

        Sxx = ((x - x.mean())**2).sum()
        SE_beta1 = s / sqrt(Sxx)

        # build confidence interval
        t_crit = t.isf(0.025, df=n - 2)
        beta1 = reg.coef_[0][0]

        lower_bound = beta1 - t_crit * SE_beta1
        upper_bound = beta1 + t_crit * SE_beta1

        deriv_reg_results.loc[len(deriv_reg_results)] = [file[:-4], reg.intercept_[0], beta1, (lower_bound, upper_bound)]


        # -------------------------------
        # STANDARD QUADRATIC REGRESSION
        # -------------------------------

        # get yearly level
        sea_level = df['sea level']
        n = len(sea_level)

        # construct independent variables
        x = np.arange(n)
        x = np.array([x, x**2])
        y = sea_level.to_numpy().reshape(-1, 1)


        # fit regression
        reg.fit(x.T, y)
        y_hat = reg.predict(x.T)

        # compute residuals and standard error
        residuals = y - y_hat
        s_squared = (residuals**2).sum() / (n - 3)
        s = sqrt(s_squared)

        X_design = np.column_stack((np.ones(n), x[0], x[1]))
        XtX_inv = np.linalg.inv(X_design.T @ X_design)

        SE_beta1 = sqrt(XtX_inv[1][1]*s)
        SE_beta2 = sqrt(XtX_inv[2][2]*s)

        # build confidence interval
        t_crit = t.isf(0.025, df=n - 3)
        beta1 = reg.coef_[0][0]
        beta2 = reg.coef_[0][1]

        lower_slope = beta1 - t_crit * SE_beta1
        upper_slope = beta1 + t_crit * SE_beta1
        lower_acc = beta2 - t_crit * SE_beta2
        upper_acc = beta2 + t_crit * SE_beta2

        quadratic_results.loc[len(quadratic_results)] = [file[:-4], reg.intercept_[0], beta1, beta2, (lower_acc, upper_acc)]
        

        # -------------------------------------
        # ESTIMATES ON DERIVATIVE OF QUADRATIC
        # -------------------------------------
        g = np.array([np.zeros(n), beta1*np.ones(n), 2*beta2*np.arange(n)]).T

        dir_var = s_squared * np.sum((g @ XtX_inv) * g, axis=1)
        
        f_critical = f.isf(0.05, 3, n-3)
        lower_deriv = np.sum(g, axis=1) - np.sqrt(dir_var*3*f_critical)
        upper_deriv = np.sum(g, axis=1) + np.sqrt(dir_var*3*f_critical)
        
        change_rate_estimate = pd.DataFrame({'date': df['date']
                                            ,'rate': np.sum(g, axis=1)
                                            ,'lower bound':lower_deriv
                                            ,'upper bound':upper_deriv})
        change_rate_estimate.to_csv(f'.\\Results\\{file[:4]} - rate of change.csv', index=False)


    deriv_reg_results.to_csv('.\\Results\\derivative regression.csv', index=False)
    quadratic_results.to_csv('.\\Results\\quadratic regression.csv', index=False)
