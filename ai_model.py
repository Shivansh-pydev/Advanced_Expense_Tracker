import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ================= PREDICT NEXT EXPENSE =================
def predict_future_expense(df):

    if df.empty:
        return None

    df = df.copy()
    df['Index'] = np.arange(len(df))

    X = df[['Index']]
    y = df['Amount']

    model = LinearRegression()
    model.fit(X, y)

    future = model.predict([[len(df)]])[0]

    return round(future, 2)


# ================= SPENDING TREND =================
def spending_trend(df):

    if df.empty or len(df) < 2:
        return "Not enough data"

    if df['Amount'].iloc[-1] > df['Amount'].iloc[-2]:
        return "📈 Spending Increasing"

    elif df['Amount'].iloc[-1] < df['Amount'].iloc[-2]:
        return "📉 Spending Decreasing"

    else:
        return "➖ Spending Stable"
