import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


# ==================================================
# 📅 MONTHLY AI FORECAST
# ==================================================
def monthly_forecast(df):
    """
    Predict next month's spending based on past data.
    Returns:
        monthly_df , prediction_value
    """

    if df is None or df.empty:
        return None, None

    try:
        # Work on copy (never modify original dataframe)
        data = df.copy()

        data["Date"] = pd.to_datetime(data["Date"])
        data["Month"] = data["Date"].dt.to_period("M")

        # Aggregate monthly spending
        monthly = data.groupby("Month")["Amount"].sum().reset_index()

        # Need at least 2 months for ML
        if len(monthly) < 2:
            return monthly, None

        monthly["Index"] = np.arange(len(monthly))

        X = monthly[["Index"]]
        y = monthly["Amount"]

        model = LinearRegression()
        model.fit(X, y)

        future_index = np.array([[len(monthly)]])
        prediction = model.predict(future_index)[0]

        if prediction < 0:
            prediction = 0

        return monthly, round(float(prediction), 2)

    except Exception as e:
        print("Monthly Forecast Error:", e)
        return None, None


# ==================================================
# 💰 SMART BUDGET ALERT SYSTEM
# ==================================================
def budget_alert(df, limit=5000):
    """
    AI-style spending warning.
    """

    if df is None or df.empty:
        return "No data available"

    try:
        total = df["Amount"].sum()

        if total > limit:
            return f"🚨 Budget exceeded! ₹{round(total,2)} spent"
        elif total > limit * 0.7:
            return f"⚠️ Approaching budget limit ₹{round(total,2)}"
        else:
            return "✅ Budget under control"

    except Exception as e:
        print("Budget Alert Error:", e)
        return "Alert unavailable"
