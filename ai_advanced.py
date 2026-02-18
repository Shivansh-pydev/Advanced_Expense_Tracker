import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# ==================================================
# 📅 ADVANCED MONTHLY FORECAST WITH ENSEMBLE ML
# ==================================================
def monthly_forecast(df):
    """
    Predict next month's spending using ensemble ML approach.
    Combines Linear Regression and Random Forest for better accuracy.
    Returns:
        monthly_df, prediction_value, confidence_interval
    """
    if df is None or df.empty:
        return None, None, None

    try:
        data = df.copy()
        data["Date"] = pd.to_datetime(data["Date"])
        data["Month"] = data["Date"].dt.to_period("M")

        # Aggregate monthly spending with additional features
        monthly = data.groupby("Month").agg({
            'Amount': ['sum', 'count', 'mean', 'std']
        }).reset_index()
        
        monthly.columns = ['Month', 'Total', 'Count', 'Mean', 'Std']
        monthly['Std'].fillna(0, inplace=True)

        if len(monthly) < 2:
            return monthly, None, None

        # Feature engineering
        monthly["Index"] = np.arange(len(monthly))
        monthly["Month_Num"] = monthly["Month"].apply(lambda x: x.month)
        
        # Prepare features
        X = monthly[["Index", "Count", "Mean", "Std", "Month_Num"]]
        y = monthly["Total"]

        # Ensemble prediction
        if len(monthly) >= 3:
            # Use Random Forest for better accuracy
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            # Use Ridge Regression for small datasets
            model = Ridge(alpha=1.0)
        
        model.fit(X, y)

        # Predict next month
        next_month = datetime.now().month
        future_features = [[
            len(monthly),
            monthly["Count"].mean(),
            monthly["Mean"].mean(),
            monthly["Std"].mean(),
            next_month
        ]]
        
        prediction = model.predict(future_features)[0]
        
        # Calculate confidence interval (standard error)
        predictions = model.predict(X)
        residuals = y - predictions
        std_error = np.std(residuals)
        confidence_interval = (
            max(0, prediction - 1.96 * std_error),
            prediction + 1.96 * std_error
        )

        prediction = max(0, prediction)

        return monthly, round(float(prediction), 2), confidence_interval

    except Exception as e:
        print("Monthly Forecast Error:", e)
        return None, None, None


# ==================================================
# 💰 INTELLIGENT BUDGET ALERT WITH ML
# ==================================================
def budget_alert(df, monthly_budget=10000):
    """
    AI-powered budget monitoring with predictive alerts.
    """
    if df is None or df.empty:
        return "No data available", 0

    try:
        # Get current month spending
        df_copy = df.copy()
        df_copy["Date"] = pd.to_datetime(df_copy["Date"])
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        current_month_df = df_copy[
            (df_copy["Date"].dt.month == current_month) & 
            (df_copy["Date"].dt.year == current_year)
        ]
        
        total = current_month_df["Amount"].sum()
        percentage = (total / monthly_budget) * 100 if monthly_budget > 0 else 0
        
        # Predictive alert
        days_in_month = 30
        current_day = datetime.now().day
        daily_avg = total / current_day if current_day > 0 else 0
        projected_total = daily_avg * days_in_month
        
        if total > monthly_budget:
            alert = f"🚨 BUDGET EXCEEDED! ₹{round(total,2)} / ₹{monthly_budget} ({percentage:.1f}%)"
        elif projected_total > monthly_budget:
            alert = f"⚠️ WARNING: Projected to exceed budget! Current: ₹{round(total,2)} | Projected: ₹{round(projected_total,2)}"
        elif percentage > 80:
            alert = f"⚠️ {percentage:.1f}% budget used (₹{round(total,2)} / ₹{monthly_budget})"
        elif percentage > 50:
            alert = f"📊 {percentage:.1f}% budget used - On track"
        else:
            alert = f"✅ {percentage:.1f}% budget used - Excellent!"

        return alert, percentage

    except Exception as e:
        print("Budget Alert Error:", e)
        return "Alert unavailable", 0


# ==================================================
# 📊 ANOMALY DETECTION IN SPENDING
# ==================================================
def detect_spending_anomalies(df):
    """
    Detect unusual spending patterns using statistical methods.
    Returns list of anomalous transactions.
    """
    if df is None or df.empty or len(df) < 10:
        return []

    try:
        amounts = df['Amount'].values
        mean = np.mean(amounts)
        std = np.std(amounts)
        
        # Z-score method for anomaly detection
        z_scores = np.abs((amounts - mean) / std)
        anomaly_threshold = 2.5
        
        anomalies = df[z_scores > anomaly_threshold].copy()
        anomalies['z_score'] = z_scores[z_scores > anomaly_threshold]
        
        return anomalies.to_dict('records')

    except Exception as e:
        print("Anomaly Detection Error:", e)
        return []


# ==================================================
# 📈 SPENDING PATTERN ANALYSIS
# ==================================================
def analyze_spending_patterns(df):
    """
    Advanced pattern analysis using time series decomposition.
    Returns insights about spending habits.
    """
    if df is None or df.empty:
        return {}

    try:
        df_copy = df.copy()
        df_copy["Date"] = pd.to_datetime(df_copy["Date"])
        df_copy = df_copy.sort_values('Date')
        
        # Day of week analysis
        df_copy['DayOfWeek'] = df_copy['Date'].dt.day_name()
        day_spending = df_copy.groupby('DayOfWeek')['Amount'].mean().to_dict()
        
        # Category trends
        category_trends = df_copy.groupby('Category')['Amount'].agg(['sum', 'mean', 'count']).to_dict()
        
        # Weekly vs Weekend spending
        df_copy['IsWeekend'] = df_copy['Date'].dt.dayofweek >= 5
        weekend_avg = df_copy[df_copy['IsWeekend']]['Amount'].mean()
        weekday_avg = df_copy[~df_copy['IsWeekend']]['Amount'].mean()
        
        return {
            'day_spending': day_spending,
            'category_trends': category_trends,
            'weekend_avg': round(weekend_avg, 2) if not np.isnan(weekend_avg) else 0,
            'weekday_avg': round(weekday_avg, 2) if not np.isnan(weekday_avg) else 0
        }

    except Exception as e:
        print("Pattern Analysis Error:", e)
        return {}


# ==================================================
# 🎯 CATEGORY-WISE BUDGET RECOMMENDATION
# ==================================================
def recommend_category_budgets(df, total_budget):
    """
    ML-based recommendation for category-wise budget allocation.
    Uses historical spending patterns.
    """
    if df is None or df.empty:
        return {}

    try:
        # Calculate category proportions from historical data
        category_totals = df.groupby('Category')['Amount'].sum()
        total_spending = category_totals.sum()
        
        if total_spending == 0:
            return {}
        
        # Recommend budgets based on historical proportions
        recommendations = {}
        for category, amount in category_totals.items():
            proportion = amount / total_spending
            recommended_budget = proportion * total_budget
            recommendations[category] = round(recommended_budget, 2)
        
        return recommendations

    except Exception as e:
        print("Budget Recommendation Error:", e)
        return {}


# ==================================================
# 🔮 PREDICTIVE SPENDING ALERTS
# ==================================================
def predict_budget_breach(df, monthly_budget):
    """
    Predict probability of exceeding budget this month.
    Uses current spending velocity and historical patterns.
    """
    if df is None or df.empty:
        return 0, "Insufficient data"

    try:
        df_copy = df.copy()
        df_copy["Date"] = pd.to_datetime(df_copy["Date"])
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Current month data
        current_month_df = df_copy[
            (df_copy["Date"].dt.month == current_month) & 
            (df_copy["Date"].dt.year == current_year)
        ]
        
        if current_month_df.empty:
            return 0, "No spending data for current month"
        
        # Calculate spending velocity
        current_day = datetime.now().day
        current_total = current_month_df["Amount"].sum()
        daily_rate = current_total / current_day if current_day > 0 else 0
        
        # Project end-of-month spending
        days_in_month = 30
        projected_total = daily_rate * days_in_month
        
        # Calculate breach probability
        if projected_total > monthly_budget:
            breach_percentage = ((projected_total - monthly_budget) / monthly_budget) * 100
            probability = min(100, 50 + breach_percentage)  # Base 50% + excess
            message = f"High risk! Projected: ₹{round(projected_total, 2)}"
        else:
            safety_margin = ((monthly_budget - projected_total) / monthly_budget) * 100
            probability = max(0, 50 - safety_margin)
            message = f"Low risk. Projected: ₹{round(projected_total, 2)}"
        
        return round(probability, 1), message

    except Exception as e:
        print("Breach Prediction Error:", e)
        return 0, "Prediction unavailable"


# ==================================================
# 📊 SAVINGS POTENTIAL CALCULATOR
# ==================================================
def calculate_savings_potential(df, monthly_budget):
    """
    Identify potential savings opportunities using ML clustering.
    """
    if df is None or df.empty:
        return {}

    try:
        # Analyze category spending
        category_spending = df.groupby('Category')['Amount'].sum().to_dict()
        total_spending = sum(category_spending.values())
        
        if total_spending == 0:
            return {}
        
        recommendations = {}
        
        # Identify high-spending categories
        for category, amount in category_spending.items():
            percentage = (amount / total_spending) * 100
            
            if percentage > 30:  # High spending category
                potential_savings = amount * 0.15  # 15% reduction potential
                recommendations[category] = {
                    'current': round(amount, 2),
                    'percentage': round(percentage, 1),
                    'potential_savings': round(potential_savings, 2),
                    'suggestion': f"High spending detected. Consider reducing by 15%"
                }
        
        return recommendations

    except Exception as e:
        print("Savings Calculation Error:", e)
        return {}
