import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def monthly_forecast(df):

    if df.empty:
        return None, None

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    monthly = df.groupby('Month')['Amount'].sum().reset_index()
    monthly['Index'] = np.arange(len(monthly))

    X = monthly[['Index']]
    y = monthly['Amount']

    model = LinearRegression()
    model.fit(X,y)

    future_index = [[len(monthly)]]
    prediction = model.predict(future_index)[0]

    return monthly, round(prediction,2)

def budget_alert(df, limit=5000):

    if df.empty:
        return None

    total = df['Amount'].sum()

    if total > limit:
        return f"⚠️ Budget exceeded! ₹{round(total,2)}"
    elif total > limit*0.7:
        return f"⚠️ Approaching limit ₹{round(total,2)}"
    else:
        return "✅ Budget under control"
