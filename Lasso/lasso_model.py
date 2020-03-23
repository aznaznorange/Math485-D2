from lib.crxXGBoost import crx_data

import numpy as np
from sklearn.linear_model import Lasso
# from sklearn.model_selection import GridSearchCV

frame = ['Male', 'Age', 'Debt', 'Married',
             'BankCustomer', 'EducationLevel',
             'Ethnicity', 'YearsEmployed', 'PriorDefault',
             'Employed', 'CreditScore', 'DriversLicense',
             'Citizen', 'ZipCode', 'Income', 'Approved']

def main():
    lasso = Lasso(
        # tol=1e-4,
        # max_iter=1e6,
        alpha=0.01
    )

    # parameters = {
    #     'alpha': [1e-25, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]
    # }
    #
    # lasso_regressor = GridSearchCV(lasso,
    #                                parameters,
    #                                scoring='neg_mean_squared_error',
    #                                cv=4)

    np_data = np.array(crx_data)

    dataX = np_data[:, 0:-1]
    dataY = np_data[:, -1]

    # lasso_regressor.fit(dataX, dataY)
    #
    # print(lasso_regressor.best_params_)
    # print(lasso_regressor.best_score_)

    lasso.fit(dataX, dataY)
    print(lasso.coef_)
    print(lasso.intercept_)

    top = []
    coefs = list(lasso.coef_)
    for i in range(len(coefs)):
        coefs[i] = abs(coefs[i])
    for i in range(8):
        index = coefs.index(max(coefs))
        print(frame[index])
        coefs[index] = 0

main()