import xgboost as xgb
from lib.crxXGBoost import crx_data
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score

# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder

frame = ['Male', 'Age', 'Debt', 'Married',
             'BankCustomer', 'EducationLevel',
             'Ethnicity', 'YearsEmployed', 'PriorDefault',
             'Employed', 'CreditScore', 'DriversLicense',
             'Citizen', 'ZipCode', 'Income', 'Approved']

def main():
    np_data = np.array(crx_data)

    data_x = np_data[:, 0:-1]
    data_y = np_data[:, -1]

    print("Model 1 (all identifiers)")
    modelKValidation(data_x, data_y)

    print("Model 2 (top 2 most influential IDs by lasso")
    data_x2 = data_x[:, 8:10]
    modelKValidation(data_x2, data_y)

    print("Model 3 (top 5 most influential IDs by lasso)")
    #Ethnicity, YearsEmployed, PriorDefault, Employed, CreditScore
    data_x3 = data_x[:, 6:11]
    modelKValidation(data_x3, data_y)

    print("Model 4 Kuhn (Prior Default, employed, credit, income)")
    data_x4 = data_x[:, [8, 9, 10, 14]]
    modelKValidation(data_x4, data_y)

    print("Model 5 (6 most by CART)")
    data_x4 = data_x[:, [2, 8, 9, 12, 13, 14]]
    modelKValidation(data_x4, data_y)

def modelKValidation(data_x, data_y):
    splits = 5
    kf = KFold(n_splits=splits, random_state=7, shuffle=True)
    xg_model = xgb.XGBClassifier(n_estimators=80,
                                 max_depth=2)
    total_cor = 0

    for train, test in kf.split(data_x):
        x_train, x_test = data_x[train], data_x[test]
        y_train, y_test = data_y[train], data_y[test]
        xg_model.fit(x_train, y_train)
        y_pred = [round(value) for value in xg_model.predict(x_test)]
        for i in range(len(y_pred)):
            if y_pred[i] == y_test[i]:
                total_cor = total_cor + 1

    average_acc = total_cor/len(data_x)
    print("Accuracy: %.2f%%" % (average_acc * 100.0))

# def modelKValidation(data_x, data_y):
#     splits = 5
#     kf = KFold(n_splits=splits, random_state=7, shuffle=True)
#     xg_model = xgb.XGBClassifier()
#     totalAcc = 0.0
#
#     for train, test in kf.split(data_x):
#         x_train, x_test = data_x[train], data_x[test]
#         y_train, y_test = data_y[train], data_y[test]
#         xg_model.fit(x_train, y_train)
#         y_pred = [round(value) for value in xg_model.predict(x_test)]
#         accuracy = accuracy_score(y_test, y_pred)
#         totalAcc = totalAcc + accuracy
#
#     averageAcc = totalAcc/splits
#     print("Accuracy: %.2f%%" % (averageAcc * 100.0))

main()