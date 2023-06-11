# Packages related to general operating system & warnings
import os
import warnings

import joblib

# Packages related to data importing, manipulation, exploratory data #analysis, data understanding
import numpy as np
import pandas as pd

# Packages related to data visualizaiton
from pandas import DataFrame, Series
from sklearn import metrics
from sklearn.ensemble import (
    AdaBoostClassifier,
    AdaBoostRegressor,
    BaggingClassifier,
    BaggingRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import MissingIndicator, SimpleImputer
from sklearn.linear_model import (
    ElasticNet,
    Lasso,
    LinearRegression,
    LogisticRegression,
    Ridge,
)
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import (
    FunctionTransformer,
    KBinsDiscretizer,
    LabelBinarizer,
    LabelEncoder,
    MaxAbsScaler,
    MinMaxScaler,
    OneHotEncoder,
    OrdinalEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.svm import SVC, SVR, LinearSVC, LinearSVR
from sklearn.tree import (  # export,; export_graphviz,
    DecisionTreeClassifier,
    DecisionTreeRegressor,
)
from termcolor import colored as cl  # text customization
from xgboost import XGBClassifier

data = pd.read_csv("creditcard.csv")
Total_transactions = len(data)
normal = len(data[data.Class == 0])
fraudulent = len(data[data.Class == 1])
fraud_percentage = round(fraudulent / normal * 100, 2)
print(
    cl("Total number of Trnsactions are {}".format(Total_transactions), attrs=["bold"])
)
print(cl("Number of Normal Transactions are {}".format(normal), attrs=["bold"]))
print(cl("Number of fraudulent Transactions are {}".format(fraudulent), attrs=["bold"]))
print(
    cl(
        "Percentage of fraud Transactions is {}".format(fraud_percentage),
        attrs=["bold"],
    )
)

data.info()

sc = StandardScaler()
amount = data["Amount"].values
data["Amount"] = sc.fit_transform(amount.reshape(-1, 1))

data.drop(["Time"], axis=1, inplace=True)

data.drop_duplicates(inplace=True)

X = data.drop("Class", axis=1).values
y = data["Class"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=1
)

DT = DecisionTreeClassifier(max_depth=4, criterion="entropy")
DT.fit(X_train, y_train)
tree_yhat = DT.predict(X_test)

print("F1 score of the Decision Tree model is {}".format(f1_score(y_test, tree_yhat)))

confusion_matrix(y_test, tree_yhat, labels=[0, 1])

n = 7
KNN = KNeighborsClassifier(n_neighbors=n)
KNN.fit(X_train, y_train)
knn_yhat = KNN.predict(X_test)

print(
    "Accuracy score of the K-Nearest Neighbors model is {}".format(
        accuracy_score(y_test, knn_yhat)
    )
)

print(
    "F1 score of the K-Nearest Neighbors model is {}".format(f1_score(y_test, knn_yhat))
)

lr = LogisticRegression()
lr.fit(X_train, y_train)
lr_yhat = lr.predict(X_test)

print(
    "Accuracy score of the Logistic Regression model is {}".format(
        accuracy_score(y_test, lr_yhat)
    )
)

print(
    "F1 score of the Logistic Regression model is {}".format(f1_score(y_test, lr_yhat))
)

svm = SVC()
svm.fit(X_train, y_train)
svm_yhat = svm.predict(X_test)

print(
    "Accuracy score of the Support Vector Machines model is {}".format(
        accuracy_score(y_test, svm_yhat)
    )
)

print(
    "F1 score of the Support Vector Machines model is {}".format(
        f1_score(y_test, svm_yhat)
    )
)

joblib.dump(svm, "./svm.joblib")

rf = RandomForestClassifier(max_depth=4)
rf.fit(X_train, y_train)
rf_yhat = rf.predict(X_test)

print(
    "Accuracy score of the Random Forest model is {}".format(
        accuracy_score(y_test, rf_yhat)
    )
)

print("F1 score of the Random Forest model is {}".format(f1_score(y_test, rf_yhat)))

xgb = XGBClassifier(max_depth=4)
xgb.fit(X_train, y_train)
xgb_yhat = xgb.predict(X_test)

print(
    "Accuracy score of the XGBoost model is {}".format(accuracy_score(y_test, xgb_yhat))
)

print("F1 score of the XGBoost model is {}".format(f1_score(y_test, xgb_yhat)))
