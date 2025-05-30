import os
import random
import mlflow
import numpy as np
import random as python_random
import tensorflow
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, InputLayer
from keras.utils import to_categorical
from keras.models import Sequential
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def reset_seeds():
   os.environ['PYTHONHASHSEED']=str(42)
   tf.random.set_seed(42)
   np.random.seed(42)
   random.seed(42)


def read_data():
  data = pd.read_csv('https://raw.githubusercontent.com/renansantosmendes/lectures-cdas-2023/master/fetal_health_reduced.csv')
  X = data.drop(["fetal_health"], axis=1)
  y = data["fetal_health"]
  return X, y


def process_data(X, y):
  columns_names = list(X.columns)
  scaler = preprocessing.StandardScaler()
  X_df = scaler.fit_transform(X)
  X_df = pd.DataFrame(X_df, columns=columns_names)

  X_train, X_test, y_train, y_test = train_test_split(X_df,
                                                      y,
                                                      test_size=0.3,
                                                      random_state=42)

  y_train = y_train -1
  y_test = y_test - 1
  return X_train, X_test, y_train, y_test


def create_model(X):
  reset_seeds()
  model = Sequential()
  model.add(InputLayer(input_shape=(X .shape[1], )))
  model.add(Dense(10, activation='relu'))
  model.add(Dense(10, activation='relu'))
  model.add(Dense(3, activation='softmax'))

  model.compile(loss='sparse_categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
  return model


def config_mlflow():
  os.environ['MLFLOW_TRACKING_USERNAME'] = 'rodrigo.peri'
  os.environ['MLFLOW_TRACKING_PASSWORD'] = '2482efab4b75da0f7887bbeccdd572c0e9887411'
  mlflow.set_tracking_uri('https://dagshub.com/rodrigo.peri/mlops-ead.mlflow')

  mlflow.tensorflow.autolog(log_models=True,
                            log_input_examples=True,
                            log_model_signatures=True)



def train_model(model, X_train, y_train, is_train=True):
  with mlflow.start_run(run_name='experiment_mlops_ead') as run:
    model.fit(X_train,
              y_train,
              epochs=50,
              validation_split=0.2,
              verbose=3)


def train_model2(model, X_train, y_train, is_train=True):
  X_train = X_train.to_numpy() if isinstance(X_train, pd.DataFrame) else X_train
  y_train = y_train.to_numpy() if isinstance(y_train, pd.Series) else y_train

  with mlflow.start_run(run_name='experiment_mlops_ead') as run:
    model.fit(X_train,
              y_train,
              epochs=50,
              validation_split=0.2,
              verbose=3)


if __name__ == "__main__":
  X, y = read_data()
  X_train, X_test, y_train, y_test = process_data(X, y)
  model = create_model(X)
  config_mlflow()
  #train_model(model, X_train, y_train)
  train_model2(model, X_train, y_train)