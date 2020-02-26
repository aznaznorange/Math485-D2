import xgboost as xgb
from lib.crxXGBoost import crx_data
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder

frame = ['Male', 'Age', 'Debt', 'Married',
             'BankCustomer', 'EducationLevel',
             'Ethnicity', 'YearsEmployed', 'PriorDefault',
             'Employed', 'CreditScore', 'DriversLicense',
             'Citizen', 'ZipCode', 'Income', 'Approved']

def main():
    # crx_df = pd.read_csv("crx_no_missing.csv",
    #                      names=frame,
    #                      usecols=[1,2,7,10,13,14],
    #                      engine='python')
    #
    # crx_train = crx_df[:math.floor(len(crx_df.index)*3/4)]
    # crx_test = crx_df[math.floor(len(crx_df.index)*3/4):]

    # model.fit(xTrain, yTrain)

    # dtrain = xgb.DMatrix(crx_train)
    # dtest = xgb.DMatrix(crx_test)
    #
    # param = {
    #     'booster': 'gbtree',
    #     'verbosity': 2,
    #     'eta': 0.3,
    #     'max_depth': 2,
    #
    # }
    # num_round = 10
    # bst = xgb.train()

    np_data = np.array(crx_data)

    data_x = np_data[:, 0:-1]
    data_y = np_data[:, -1]

    print("Model 1 (all identifiers)")
    model(data_x, data_y)

    print("Model 2 (top 2 most influential IDs by lasso")
    data_x2 = data_x[:, 8:10]
    model(data_x2, data_y)

    print("Model 3 (top 5 most influential IDs by lasso)")
    data_x3 = data_x[:, 6:11]
    model(data_x3, data_y)

    print("Model 4 (employed, credit, income)")
    data_x4 = data_x[:, [9, 10, 14]]
    model(data_x4, data_y)

def model(data_x, data_y):
    x_train, x_test, y_train, y_test = train_test_split(data_x,
                                                        data_y,
                                                        test_size=0.25,
                                                        random_state=7)

    xg_model = xgb.XGBClassifier()
    xg_model.fit(x_train, y_train)

    y_pred = [round(value) for value in xg_model.predict(x_test)]

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

main()