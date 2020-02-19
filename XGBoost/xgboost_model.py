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

    np_data = np.array(crx_data)

    dataX = np_data[:, 0:-1]
    dataY = np_data[:, -1]

    xTrain, xTest, yTrain, yTest = train_test_split(dataX,
                                                    dataY,
                                                    test_size=0.25,
                                                    random_state=7)

    model = xgb.XGBClassifier()
    model.fit(xTrain, yTrain)

    yPred = [round(value) for value in model.predict(xTest)]

    accuracy = accuracy_score(yTest, yPred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

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

main()