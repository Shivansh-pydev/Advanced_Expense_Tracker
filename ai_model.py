import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future_expense(df):

    if df.empty:
        return None

    df['Index'] = np.arange(len(df))

    X = df[['Index']]
    y = df['Amount']

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(df)]])[0]

    return round(future,2)
