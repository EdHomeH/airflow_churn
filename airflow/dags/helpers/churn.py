import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def preprocess_churn(data_path: str, base_path: str) -> (str, str):

    y_path = os.path.join(base_path, 'data/Telco/preproced_churn/y.csv')
    x_path = os.path.join(base_path, 'data/Telco/preproced_churn/X.csv')

    telec_df = pd.read_csv(data_path)

    telec_df.TotalCharges = pd.to_numeric(telec_df.TotalCharges, errors='coerce')

    telec_df.dropna(inplace=True)
    df2=telec_df.iloc[:, 1:]
    df2['Churn'].replace(to_replace='Yes', value=1, inplace=True)
    df2['Churn'].replace(to_replace='No', value=0, inplace=True)

    df_dumb = pd.get_dummies(df2)

    # save y
    df_dumb[['Churn']].to_csv(y_path, index=False)

    # scale X
    X = df_dumb.drop(columns='Churn')
    features = X.columns.values
    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit(X)
    X = pd.DataFrame(scaler.transform(X))
    X.columns = features

    # save X
    X.to_csv(x_path, index=False)

    return x_path, y_path


def train_model(x_path, y_path):

    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    model = LogisticRegression()
    result = model.fit(X_train, y_train)

    prediction_test = model.predict(X_test)

    print(metrics.accuracy_score(y_test, prediction_test))
