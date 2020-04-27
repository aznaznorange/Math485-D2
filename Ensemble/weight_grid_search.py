import xgboost as xgb
from lib.crxXGBoost import crx_data
import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from statistics import mode

np_data = np.array(crx_data)

feature = np_data[:, 0:-1]
target = np_data[:, -1]


# weighted average
def ensemble3(pred1, pred2, pred3, c1, c2, c3):
    y_final = []
    for i in range(len(pred1)):
        prob = (c1*pred1[i][0] + c2*pred2[i][0] + c3*pred3[i][0]) / (c1 + c2 + c3)
        if prob > 0.5:
            y_final.append(0)
        else:
            y_final.append(1)

    return y_final


def model_kvalidation(data_x, data_y, c1, c2, c3):
    model1 = xgb.XGBClassifier(n_estimators=80,
                               max_depth=2)

    model2 = SVC(kernel='rbf',
                 probability=True,
                 class_weight='balanced',
                 gamma='scale')

    # model3 = tree.DecisionTreeClassifier()
    model3 = LogisticRegression()

    kf = KFold(n_splits=10, random_state=7, shuffle=True)

    ens3_cor = 0

    for train, test in kf.split(data_x):
        x_train, x_test = data_x[train], data_x[test]
        y_train, y_test = data_y[train], data_y[test]

        x_train_5lasso = x_train[:, 6:11]
        x_train_6cart = x_train[:, [2, 8, 9, 12, 13, 14]]
        x_test_5lasso = x_test[:, 6:11]
        x_test_6cart = x_test[:, [2, 8, 9, 12, 13, 14]]

        model1.fit(x_train_6cart, y_train)
        model2.fit(x_train_5lasso, y_train)
        model3.fit(x_train_5lasso, y_train)

        y_prob1 = model1.predict_proba(x_test_6cart)
        y_prob2 = model2.predict_proba(x_test_5lasso)
        y_prob3 = model3.predict_proba(x_test_5lasso)

        y_pred_ens3 = ensemble3(y_prob1, y_prob2, y_prob3, c1, c2, c3)     # values found by quick grid search

        for i in range(len(y_pred_ens3)):
            if y_pred_ens3[i] == y_test[i]:
                ens3_cor = ens3_cor + 1

    return ens3_cor


co1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
co2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
co3 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
max_cor = 0

for i in range(len(co1)):
    for j in range(len(co2)):
        for k in range(len(co3)):
            cor = model_kvalidation(feature, target, co1[i], co2[j], co3[k])
            if cor > max_cor:
                max_cor = cor
                print([co1[i], co2[j], co3[k]])
