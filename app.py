import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from pdf_report import create_pdf

from utils import (
    initialize_csv,
    save_expense,
    load_expenses,
    get_total_expenses,
    get_category_summary,
    get_expense_by_category
)

from auth import create_users_table, register_user, login_user
from ai_model import predict_future_expense, spending_trend
from ai_advanced import monthly_forecast, budget_alert


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SAAS UI STYLE =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#020617,#0f172a);
}

[data-testid="stSidebar"] {
    background: #020617;
}

[data-testid="stMetric"] {
    background: rgba(30,41,59,0.7) !important;
    border-radius:18px;
    padding:20px;
    backdrop-filter: blur(16px);
    box-shadow:0 10px 25px rgba(0,0,0,0.5);
}

h1 {
    background: linear-gradient(90deg,#3b82f6,#06b6d4);
    -webkit-background-clip:text;
    color:transparent;
    font-weight:800;
}

.stButton>button {
    background: linear-gradient(90deg,#3b82f6,#06b6d4);
    color:white;
    border:none;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)


# ================= LOGIN SYSTEM =================
create_users_table()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.markdown("<h1>🔐 Secure Login</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Register"):
            ok = register_user(new_user, new_pass)
            if ok:
                st.success("User registered successfully! Login now.")
            else:
                st.error("Username already exists")

    st.stop()


# ================= INIT USER FILE =================
initialize_csv(st.session_state.user)


# ================= SIDEBAR =================
st.sidebar.markdown("## 📊 Navigation")

st.sidebar.markdown(
    f"""
    <div style='padding:14px;border-radius:14px;
    background:rgba(59,130,246,0.15);text-align:center;font-weight:600'>
    👤 {st.session_state.user}
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.rerun()

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard","➕ Add Expense","📈 Analytics"]
)

# ================= DASHBOARD =================
if page == "🏠 Dashboard":

    st.markdown("<h1>💰 Expense Intelligence Dashboard</h1>", unsafe_allow_html=True)

    df = load_expenses(st.session_state.user)

    # ================= 🤖 AI INSIGHTS PANEL =================
    st.markdown("## 🤖 AI Insights")

    if not df.empty:

        future = predict_future_expense(df)
        trend = spending_trend(df)
        monthly_data, forecast = monthly_forecast(df)
        alert = budget_alert(df)

        st.markdown(f"""
        <div style="
            background:rgba(30,41,59,0.65);
            padding:22px;
            border-radius:18px;
            backdrop-filter:blur(16px);
            box-shadow:0 10px 30px rgba(0,0,0,0.45);
            font-size:16px;
            line-height:1.7;
        ">
            🔮 <b>Predicted Next Expense:</b> ₹{future if future else 'N/A'} <br>
            📊 <b>Spending Trend:</b> {trend} <br>
            📅 <b>Next Month Forecast:</b> ₹{forecast if forecast else 'N/A'} <br>
            💰 <b>Budget Status:</b> {alert}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ================= METRICS =================
    if df.empty:
        st.warning("No expenses yet. Add one!")
    else:

        col1, col2, col3 = st.columns(3)

        total = get_total_expenses(df)
        num_transactions = len(df)
        avg = total / num_transactions if num_transactions else 0

        col1.metric("💵 Total Expenses", f"Rs.{total:,.2f}")
        col2.metric("📝 Transactions", num_transactions)
        col3.metric("📊 Average Expense", f"Rs.{avg:,.2f}")

        st.markdown("---")

        # ================= TABLE =================
        st.subheader("📋 Recent Expenses")

        display_df = df.copy()
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"Rs.{x:,.2f}")
        display_df = display_df.sort_values('Date', ascending=False)

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ================= EXPORT BUTTONS =================
        csv = df.to_csv(index=False).encode('utf-8')

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📥 Download CSV",
                data=csv,
                file_name="expenses.csv",
                mime="text/csv"
            )

        with col2:
            pdf_path = f"report_{st.session_state.user}.pdf"

            if st.button("📄 Generate PDF Report"):
                create_pdf(pdf_path, df)

            try:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=f,
                        file_name="Expense_Report.pdf",
                        mime="application/pdf"
                    )
            except:
                pass


# ================= ADD EXPENSE =================
elif page == "➕ Add Expense":

    st.title("➕ Add New Expense")

    with st.form("expense_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("📅 Date", value=datetime.now())
            category = st.selectbox(
                "🏷️ Category",
                ["Food","Travel","Shopping","Bills","Health","Other"]
            )

        with col2:
            amount = st.number_input("💵 Amount", min_value=0.01)
            note = st.text_input("📝 Note")

        submitted = st.form_submit_button("Add Expense")

        if submitted:
            save_expense(
                st.session_state.user,
                date,
                category,
                amount,
                note
            )
            st.success("Expense Added!")
            st.balloons()


# ================= ANALYTICS + AI =================
elif page == "📈 Analytics":

    st.title("📈 Expense Analytics")

    df = load_expenses(st.session_state.user)

    if df.empty:
        st.warning("Add expenses first!")
    else:

        summary = get_category_summary(df)

        col1, col2 = st.columns(2)
        col1.metric("Total Spending", f"Rs.{get_total_expenses(df):,.2f}")
        col2.metric("Top Category", summary.idxmax())

        st.markdown("## 🤖 AI Expense Intelligence")

        future = predict_future_expense(df)
        trend = spending_trend(df)

        c1, c2 = st.columns(2)

        if future:
            c1.metric("🔮 Predicted Next Expense", f"Rs.{future}")

        c2.info(trend)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots()
            ax1.pie(summary, labels=summary.index, autopct='%1.1f%%')
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots()
            ax2.bar(summary.index, summary.values)
            plt.xticks(rotation=45)
            st.pyplot(fig2)


# ================= FOOTER =================
st.sidebar.markdown("---")
st.sidebar.info("Expense Tracker with AI 🚀")
