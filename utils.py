import pandas as pd
import os


# ==================================================
# 📂 USER FILE SYSTEM
# ==================================================
def get_user_file(username):
    """
    Create per-user expense file.
    """
    if username is None:
        return "expenses_guest.csv"
    return f"expenses_{username}.csv"


# ==================================================
# 🧾 INITIALIZE CSV
# ==================================================
def initialize_csv(username):

    CSV_FILE = get_user_file(username)

    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Date","Category","Amount","Note"])
        df.to_csv(CSV_FILE, index=False)


# ==================================================
# ➕ SAVE EXPENSE
# ==================================================
def save_expense(username, date, category, amount, note):

    CSV_FILE = get_user_file(username)

    try:
        new_expense = {
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": round(float(amount), 2),
            "Note": note.strip()
        }

        new_df = pd.DataFrame([new_expense])

        # Check if file exists to decide header
        file_exists = os.path.exists(CSV_FILE)

        new_df.to_csv(
            CSV_FILE,
            mode="a",
            header=not file_exists,
            index=False
        )

        return True

    except Exception as e:
        print("Save Expense Error:", e)
        return False


# ==================================================
# 📥 LOAD EXPENSES
# ==================================================
def load_expenses(username):

    CSV_FILE = get_user_file(username)

    try:
        if os.path.exists(CSV_FILE):

            df = pd.read_csv(CSV_FILE)

            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"])
                df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

            return df

        return pd.DataFrame(columns=["Date","Category","Amount","Note"])

    except Exception as e:
        print("Load Error:", e)
        return pd.DataFrame(columns=["Date","Category","Amount","Note"])


# ==================================================
# 💰 TOTAL EXPENSES
# ==================================================
def get_total_expenses(df):

    if df is None or df.empty:
        return 0.0

    return round(df["Amount"].sum(), 2)


# ==================================================
# 📊 CATEGORY SUMMARY
# ==================================================
def get_category_summary(df):

    if df is None or df.empty:
        return pd.Series(dtype=float)

    category_totals = df.groupby("Category")["Amount"].sum()
    category_totals = category_totals.sort_values(ascending=False)

    return category_totals


# ==================================================
# 🔎 FILTER BY CATEGORY
# ==================================================
def get_expense_by_category(df, category):

    if df is None or df.empty:
        return df

    return df[df["Category"] == category]
