import xgboost as xgb
from lib.crxXGBoost import crx_data
import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from statistics import mode
import matlab.engine

np_data = np.array(crx_data)

feature = np_data[:, 0:-1]
target = np_data[:, -1]


# max voting
def ensemble1(pred1, pred2, pred3):
    y_final = []
    for i in range(len(pred1)):
        y_final.append(mode([pred1[i], pred2[i], pred3[i]]))

    return y_final


# average
def ensemble2(pred1, pred2, pred3):
    y_final = []
    for i in range(len(pred1)):
        avg = (pred1[i][0] + pred2[i][0] + pred3[i][0])/3
        if avg > 0.5:
            y_final.append(0)
        else:
            y_final.append(1)

    return y_final


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


def model_kvalidation(data_x, data_y):
    model1 = xgb.XGBClassifier(n_estimators=80,
                               max_depth=2)

    model2 = SVC(kernel='rbf',
                 probability=True,
                 class_weight='balanced',
                 gamma='scale')

    # model3 = tree.DecisionTreeClassifier()
    model3 = LogisticRegression()

    kf = KFold(n_splits=10, random_state=7, shuffle=True)

    ens1_cor = 0
    ens2_cor = 0
    ens3_cor = 0
    ens4_cor = 0
    xg_model_cor = 0
    svm_model_cor = 0
    cart_model_cor = 0

    for train, test in kf.split(data_x):
        x_5lasso = data_x[:, 6:11]
        x_6cart = data_x[:, [2, 8, 9, 12, 13, 14]]

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
        y_pred1 = [0 if x > 0.5 else 1 for (x, y) in y_prob1]
        y_prob2 = model2.predict_proba(x_test_5lasso)
        y_pred2 = [0 if x >= .7 else 1 for (x, y) in y_prob2]
        y_prob3 = model3.predict_proba(x_test_5lasso)
        y_pred3 = [0 if x > 0.5 else 1 for (x, y) in y_prob3]

        y_pred_ens1 = ensemble1(y_pred1, y_pred2, y_pred3)
        y_pred_ens2 = ensemble2(y_prob1, y_prob2, y_prob3)
        y_pred_ens3 = ensemble3(y_prob1, y_prob2, y_prob3, 4, 2, 1)     # values found by quick grid search

        stack1 = np.array(model1.predict(x_6cart))
        stack2 = np.array(model2.predict(x_5lasso))
        stack_feat = np.column_stack((stack1, stack2))
        model3.fit(stack_feat[train], y_train)

        y_pred_ens4 = [round(x) for x in model3.predict(stack_feat[test])]

        for i in range(len(y_pred1)):
            if y_pred_ens1[i] == y_test[i]:
                ens1_cor = ens1_cor + 1
            if y_pred_ens2[i] == y_test[i]:
                ens2_cor = ens2_cor + 1
            if y_pred_ens3[i] == y_test[i]:
                ens3_cor = ens3_cor + 1
            if y_pred_ens4[i] == y_test[i]:
                ens4_cor = ens4_cor + 1
            if y_pred1[i] == y_test[i]:
                xg_model_cor = xg_model_cor + 1
            if y_pred2[i] == y_test[i]:
                svm_model_cor = svm_model_cor + 1
            if y_pred3[i] == y_test[i]:
                cart_model_cor = cart_model_cor + 1

    average_acc = ens1_cor/len(data_x)
    print("Ensemble (max voting) Accuracy: %.2f%%" % (average_acc * 100.0))
    average_acc = ens2_cor / len(data_x)
    print("Ensemble (average) Accuracy: %.2f%%" % (average_acc * 100.0))
    average_acc = ens3_cor / len(data_x)
    print("Ensemble (weighted) Accuracy: %.2f%%" % (average_acc * 100.0))
    average_acc = ens4_cor / len(data_x)
    print("Ensemble (stack) Accuracy: %.2f%%" % (average_acc * 100.0))
    average_acc = xg_model_cor / len(data_x)
    print("XGBoost Accuracy: %.2f%%" % (average_acc * 100.0))
    average_acc = svm_model_cor / len(data_x)
    print("SVM Accuracy: %.2f%%" % (average_acc * 100.0))
    average_acc = cart_model_cor / len(data_x)
    print("LogRegression Accuracy: %.2f%%" % (average_acc * 100.0))


model_kvalidation(feature, target)