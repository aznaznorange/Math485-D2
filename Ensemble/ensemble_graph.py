import xgboost as xgb
from lib.crxXGBoost import crx_data
import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

np_data = np.array(crx_data)

feature = np_data[:, 0:-1]
target = np_data[:, -1]


# weighted average (highest accuracy)
def ensemble(pred1, pred2, pred3, c1, c2, c3):
    y_final = []
    for i in range(len(pred1)):
        prob = (c1*pred1[i][1] + c2*pred2[i][1] + c3*pred3[i][1]) / (c1 + c2 + c3)
        y_final.append(prob)

    return y_final


def make_graph(data_x, data_y):
    model1 = xgb.XGBClassifier(n_estimators=80,
                               max_depth=2)

    model2 = SVC(kernel='rbf',
                 probability=True,
                 class_weight='balanced',
                 gamma='scale')

    model3 = LogisticRegression()

    kf = KFold(n_splits=10, random_state=7, shuffle=True)

    data_x_5lasso = data_x[:, 6:11]
    data_x_6cart = data_x[:, [2, 8, 9, 12, 13, 14]]

    model1.fit(data_x_6cart, data_y)
    model2.fit(data_x_5lasso, data_y)
    model3.fit(data_x_5lasso, data_y)

    y_prob1 = model1.predict_proba(data_x_6cart)
    y_prob2 = model2.predict_proba(data_x_5lasso)
    y_prob3 = model3.predict_proba(data_x_5lasso)

    y_pred_ens = ensemble(y_prob1, y_prob2, y_prob3, 7, 4, 1)  # values found by quick grid search

    range_x = range(1, len(y_pred_ens) + 1, 1)
    range_y1 = [y for (x, y) in y_prob1]
    range_y2 = [y for (x, y) in y_prob2]
    range_y3 = [y for (x, y) in y_prob3]

    dot_size = 2

    fig = plt.figure()
    ax = plt.subplot(111)

    plt.title(label='Predictions on Data Set for High Accuracy Models')
    ax.scatter(range_x, range_y1, label='XGBoost', s=dot_size)
    ax.scatter(range_x, range_y2, label='SVM', s=dot_size)
    ax.scatter(range_x, range_y3, label='LogReg', s=dot_size)
    ax.scatter(range_x, y_pred_ens, label='Weighted', s=dot_size)
    ax.scatter(range_x, data_y, label="True Category", s=dot_size)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
    ax.legend(loc='center right',
              bbox_to_anchor=(1.3, 0.5),
              fontsize='large',
              markerscale=4)
    plt.xlabel('Data Points')
    plt.ylabel('Probability Measure')
    plt.savefig('pMeasureScatter.png')
    # plt.show()


make_graph(feature, target)