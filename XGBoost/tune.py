import xgboost as xgb
from lib.crxXGBoost import crx_data
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, GridSearchCV

def main():
    np_data = np.array(crx_data)

    data_x = np_data[:, 0:-1]
    data_y = np_data[:, -1]

    print("Model 3 (top 5 most influential IDs by lasso)")
    data_x3 = data_x[:, 6:11]
    tune_depth_and_trees(data_x3, data_y)
    # Best: -0.343346 using {'max_depth': 2, 'n_estimators': 50}

def tune_depth_and_trees(data_x, data_y):
    xg_model = xgb.XGBClassifier()
    max_depth = range(1, 6, 1)
    n_estimators = range(10, 200, 10)
    param_grid = dict(max_depth=max_depth, n_estimators=n_estimators)
    kfold = KFold(n_splits=10, shuffle=True, random_state=7)
    grid_search = GridSearchCV(xg_model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold, verbose=1)
    grid_result = grid_search.fit(data_x, data_y)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))
    # plot results
    scores = np.array(means).reshape(len(max_depth), len(n_estimators))
    for i, value in enumerate(max_depth):
        plt.plot(n_estimators, scores[i], label='depth: ' + str(value))
    plt.legend()
    plt.xlabel('n_estimators')
    plt.ylabel('Log Loss')
    plt.savefig('n_estimators_vs_max_depth.png')

def tune_max_depth(data_x, data_y):
    xg_model = xgb.XGBClassifier()
    max_depth = range(1, 6, 1)
    param_grid = dict(max_depth=max_depth)
    kfold = KFold(n_splits=10, shuffle=True, random_state=7)
    grid_search = GridSearchCV(xg_model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold, verbose=1)
    grid_result = grid_search.fit(data_x, data_y)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))
    # plot
    plt.errorbar(max_depth, means, yerr=stds)
    plt.title("XGBoost max_depth vs Log Loss")
    plt.xlabel('max_depth')
    plt.ylabel('Log Loss')
    plt.savefig('max_depth.png')

def tune_n_estimators(data_x, data_y):
    xg_model = xgb.XGBClassifier()
    n_estimators = range(10, 200, 10)
    param_grid = dict(n_estimators=n_estimators)
    kfold = KFold(n_splits=10, shuffle=True, random_state=7)
    grid_search = GridSearchCV(xg_model, param_grid,
                               scoring="neg_log_loss",
                               n_jobs=-1,
                               cv=kfold)
    grid_result = grid_search.fit(data_x, data_y)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))
    # plot
    plt.errorbar(n_estimators, means, yerr=stds)
    plt.title("XGBoost n_estimators vs Log Loss")
    plt.xlabel('n_estimators')
    plt.ylabel('Log Loss')
    plt.savefig('n_estimators.png')

main()