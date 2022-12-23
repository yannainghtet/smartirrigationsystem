import pandas as pd
import numpy as np
import pickle
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')


def WateramountPrediction(env_values):
    dataset = pd.read_csv("Groundnutmain.csv")

    X = dataset.iloc[1:1200, 0:8]
    y = dataset.iloc[1:1200, 8]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = RandomForestRegressor()
    regressor.fit(X_train, y_train)

    X_new = np.array(env_values)

    return regressor.predict(X_new)

#prediction = WateramountPrediction([[44,508,22,19,27.9,15,4.82409,0.75]])
#print(prediction)


