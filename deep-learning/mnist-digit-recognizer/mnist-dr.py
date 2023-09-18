# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 9/18/23
# Description: Main program for the digit recognizer, trained on the Kaggle dataset. Uses the model that has been configured in model.py.

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import model as md
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import accuracy_score, confusion_matrix
from keras.utils import to_categorical

import time

start_time = time.time()

# -------------------------------------Load and Prepare Training Data------------------------------------------
data = pd.read_csv("./input/train.csv")
print(data.shape)

y = data["label"]
X = data.drop("label", axis=1)

print(y.value_counts().to_dict())
y = to_categorical(y, num_classes=10)

del data

# set to grayscale values
X = X / 255.0
X = X.values.reshape(-1, 28, 28, 1)







