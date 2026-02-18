import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pdf_report import create_pdf

from utils import (
    initialize_csv,
    save_expense,
    load_expenses,
    get_total_expenses,
    get_category_summary,
    get_expense_by_category
)

from auth import (
    create_users_table, 
    register_user, 
    login_user, 
    verify_database,
    get_user_budget,
    update_user_budget,
    delete_user,
    reset_database
)

from ai_model import predict_future_expense, spending_trend
from ai_advanced import (
    monthly_forecast, 
    budget_alert,
    detect_spending_anomalies,
    analyze_spending_patterns,
    recommend_category_budgets,
    predict_budget_breach,
    calculate_savings_potential
)


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="💰 AI Expense Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= PROFESSIONAL LIGHT THEME WITH ANIMATIONS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    animation: fadeIn 0.5s ease-in;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #e8f4f8 100%);
    border-right: 1px solid #e0e7ff;
}

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: slideUp 0.6s ease-out;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 48px rgba(31, 38, 135, 0.25);
}

h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    letter-spacing: -0.5px;
    animation: slideDown 0.5s ease-out;
}

h2, h3 {
    color: #1e293b;
    font-weight: 600;
}

.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
}

.stTextInput>div>div>input,
.stSelectbox>div>div>select,
.stNumberInput>div>div>input {
    border-radius: 10px;
    border: 2px solid #e0e7ff;
    padding: 12px;
    background: white;
    transition: border-color 0.3s ease;
}

.stTextInput>div>div>input:focus,
.stSelectbox>div>div>select:focus,
.stNumberInput>div>div>input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.5);
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.stAlert {
    border-radius: 12px;
    border-left: 4px solid;
    animation: slideIn 0.4s ease-out;
}

.user-badge {
    padding: 16px;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    animation: bounceIn 0.6s ease-out;
}

.ai-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    padding: 28px;
    border-radius: 16px;
    border: 2px solid rgba(102, 126, 234, 0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
    font-size: 16px;
    line-height: 1.8;
    animation: fadeInUp 0.6s ease-out;
}

.feature-card {
    background: rgba(255, 255, 255, 0.95);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(102, 126, 234, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.budget-progress {
    height: 30px;
    background: #e0e7ff;
    border-radius: 15px;
    overflow: hidden;
    position: relative;
    margin: 16px 0;
}

.budget-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 15px;
    transition: width 0.5s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 14px;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes bounceIn {
    0% {
        opacity: 0;
        transform: scale(0.3);
    }
    50% {
        opacity: 1;
        transform: scale(1.05);
    }
    70% {
        transform: scale(0.9);
    }
    100% {
        transform: scale(1);
    }
}

.stSpinner > div {
    border-top-color: #667eea !important;
}

.ml-badge {
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 8px;
}

.anomaly-alert {
    background: rgba(239, 68, 68, 0.1);
    border: 2px solid rgba(239, 68, 68, 0.3);
    padding: 16px;
    border-radius: 12px;
    margin: 12px 0;
}

.login-container {
    background: rgba(255, 255, 255, 0.95);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
    animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}
</style>
""", unsafe_allow_html=True)


# ================= INITIALIZE DATABASE =================
create_users_table()

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "monthly_budget" not in st.session_state:
    st.session_state.monthly_budget = 10000


# ================= LOGIN SYSTEM =================
if st.session_state.user is None:

    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 AI Expense Intelligence Platform</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #64748b;'>Machine Learning Powered Personal Finance Manager</p>", unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### 🤖\n**ML Predictions**", unsafe_allow_html=True)
    with col2:
        st.markdown("### 📊\n**Anomaly Detection**", unsafe_allow_html=True)
    with col3:
        st.markdown("### 🎯\n**Smart Budgeting**", unsafe_allow_html=True)
    with col4:
        st.markdown("### 📈\n**Pattern Analysis**", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", key="login_user", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="Enter your password")

            if st.button("🚀 Login", use_container_width=True):
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.user = user[1]  # Store actual username from DB
                        st.session_state.monthly_budget = user[2]  # Store budget
                        st.success("✅ Login successful!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
            
            new_user = st.text_input("👤 Create Username", key="reg_user", placeholder="Choose a username (min 3 characters)")
            new_pass = st.text_input("🔒 Create Password", type="password", key="reg_pass", placeholder="Choose a strong password (min 4 characters)")
            confirm_pass = st.text_input("🔒 Confirm Password", type="password", key="confirm_pass", placeholder="Re-enter password")
            initial_budget = st.number_input("💰 Set Monthly Budget (₹)", min_value=1000, value=10000, step=1000)

            if st.button("📝 Register", use_container_width=True):
                # Input validation
                if not new_user or not new_pass or not confirm_pass:
                    st.warning("⚠️ Please fill all fields")
                elif len(new_user.strip()) < 3:
                    st.error("❌ Username must be at least 3 characters")
                elif new_pass != confirm_pass:
                    st.error("❌ Passwords do not match!")
                elif len(new_pass) < 4:
                    st.warning("⚠️ Password should be at least 4 characters")
                else:
                    # Attempt registration
                    with st.spinner("Creating your account..."):
                        ok = register_user(new_user.strip(), new_pass, initial_budget)
                        
                        if ok:
                            st.success(f"✅ Account created successfully! Welcome, {new_user.strip()}!")
                            st.balloons()
                            st.info("👉 Please switch to the Login tab to sign in")
                        else:
                            st.error(f"❌ Username '{new_user.strip()}' already exists. Please choose a different username.")
            
            st.markdown("</div>", unsafe_allow_html=True)

    # Debug panel with admin tools
    with st.expander("🔧 Debug: System Status & Database Tools"):
        users = verify_database()
        if users:
            st.info(f"📋 Total registered users: {len(users)}")
            
            # Show users in a nice format
            for idx, (user, budget) in enumerate(users, 1):
                st.text(f"{idx}. {user} (Budget: ₹{budget:,.0f})")
        else:
            st.warning("No users registered yet")
        
        st.markdown("---")
        st.caption("⚙️ Admin Tools (for testing)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_user = st.text_input("Username to delete", key="del_user")
            if st.button("🗑️ Delete User"):
                if test_user:
                    if delete_user(test_user):
                        st.success(f"Deleted user: {test_user}")
                        st.rerun()
                    else:
                        st.error("User not found")
        
        with col2:
            if st.button("⚠️ Reset Entire Database"):
                if reset_database():
                    st.warning("Database cleared!")
                    st.rerun()

    st.stop()


# ================= INIT USER FILE =================
initialize_csv(st.session_state.user)


# ================= SIDEBAR =================
st.sidebar.markdown("## 🎯 Navigation")

st.sidebar.markdown(
    f"""
    <div class='user-badge'>
        👤 {st.session_state.user}
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Budget Management in Sidebar
with st.sidebar.expander("💰 Budget Settings"):
    current_budget = get_user_budget(st.session_state.user)
    new_budget = st.number_input(
        "Monthly Budget (₹)", 
        min_value=1000, 
        value=int(current_budget),
        step=1000,
        key="sidebar_budget"
    )
    if st.button("Update Budget", key="update_budget_btn"):
        if update_user_budget(st.session_state.user, new_budget):
            st.session_state.monthly_budget = new_budget
            st.success("✅ Budget updated!")
            st.rerun()
        else:
            st.error("❌ Update failed")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.user = None
    st.session_state.monthly_budget = 10000
    st.rerun()

page = st.sidebar.radio(
    "📂 Select Page",
    ["🏠 Dashboard", "➕ Add Expense", "📈 Analytics", "🤖 ML Insights", "⚙️ Settings"],
    label_visibility="collapsed"
)


# ================= DASHBOARD PAGE =================
if page == "🏠 Dashboard":

    st.markdown("<h1>💰 AI Expense Intelligence Dashboard</h1>", unsafe_allow_html=True)

    df = load_expenses(st.session_state.user)
    user_budget = get_user_budget(st.session_state.user)

    # ================= BUDGET OVERVIEW =================
    st.markdown("## 💰 Monthly Budget Overview")
    
    alert_message, budget_percentage = budget_alert(df, user_budget)
    
    # Budget Progress Bar
    progress_color = "#667eea" if budget_percentage < 80 else "#f59e0b" if budget_percentage < 100 else "#ef4444"
    
    st.markdown(f"""
    <div class="budget-progress">
        <div class="budget-progress-bar" style="width: {min(budget_percentage, 100)}%; background: {progress_color};">
            {budget_percentage:.1f}%
        </div>
    </div>
    <p style="text-align: center; margin-top: 8px; color: #64748b;">
        Budget: ₹{user_budget:,.0f} | Status: {alert_message}
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= 🤖 AI INSIGHTS PANEL =================
    st.markdown("## 🤖 AI-Powered Insights <span class='ml-badge'>ML</span>", unsafe_allow_html=True)

    if not df.empty:
        future = predict_future_expense(df)
        trend = spending_trend(df)
        monthly_data, forecast, confidence = monthly_forecast(df)
        breach_prob, breach_msg = predict_budget_breach(df, user_budget)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="ai-card">
                🔮 <b>Predicted Next Expense:</b> ₹{future if future else 'N/A'} <br><br>
                📊 <b>Spending Trend:</b> {trend} <br><br>
                📅 <b>Next Month Forecast:</b> ₹{forecast if forecast else 'N/A'}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="ai-card">
                ⚠️ <b>Budget Breach Risk:</b> {breach_prob}% <br><br>
                💡 <b>Prediction:</b> {breach_msg} <br><br>
                🎯 <b>Budget Alert:</b> {alert_message.split('₹')[0]}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("🎯 Add your first expense to see AI-powered insights!")

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= METRICS =================
    if df.empty:
        st.warning("📝 No expenses recorded yet. Start tracking by adding your first expense!")
    else:
        col1, col2, col3, col4 = st.columns(4)

        total = get_total_expenses(df)
        num_transactions = len(df)
        avg = total / num_transactions if num_transactions else 0
        remaining = user_budget - total

        col1.metric("💵 Total Expenses", f"₹{total:,.2f}")
        col2.metric("📝 Transactions", num_transactions)
        col3.metric("📊 Average Expense", f"₹{avg:,.2f}")
        col4.metric("💰 Budget Remaining", f"₹{remaining:,.2f}", 
                   delta=f"{((remaining/user_budget)*100):.1f}% left" if user_budget > 0 else "0%")

        st.markdown("---")

        # ================= ANOMALY DETECTION =================
        anomalies = detect_spending_anomalies(df)
        if anomalies:
            st.markdown("### 🚨 Unusual Spending Detected <span class='ml-badge'>ML</span>", unsafe_allow_html=True)
            for anomaly in anomalies[:3]:  # Show top 3
                st.markdown(f"""
                <div class="anomaly-alert">
                    <b>⚠️ Anomaly Detected:</b> ₹{anomaly['Amount']:,.2f} on {anomaly['Date']} 
                    in category <b>{anomaly['Category']}</b><br>
                    <small>This expense is significantly higher than your typical spending pattern.</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ================= TABLE =================
        st.subheader("📋 Recent Expense History")

        display_df = df.copy()
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"₹{x:,.2f}")
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d %b %Y')
        display_df = display_df.sort_values('Date', ascending=False).head(20)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.TextColumn("📅 Date", width="medium"),
                "Category": st.column_config.TextColumn("🏷️ Category", width="medium"),
                "Amount": st.column_config.TextColumn("💰 Amount", width="medium"),
                "Note": st.column_config.TextColumn("📝 Description", width="large"),
            }
        )

        # ================= EXPORT =================
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📥 Export Your Data")

        csv = df.to_csv(index=False).encode('utf-8')
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📄 Download CSV",
                data=csv,
                file_name=f"expenses_{st.session_state.user}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            pdf_path = f"report_{st.session_state.user}.pdf"
            if st.button("📊 Generate PDF", use_container_width=True):
                try:
                    create_pdf(pdf_path, df)
                    st.success("✅ PDF Generated!")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")


# ================= ADD EXPENSE PAGE =================
elif page == "➕ Add Expense":

    st.markdown("<h1>➕ Add New Expense</h1>", unsafe_allow_html=True)
    
    user_budget = get_user_budget(st.session_state.user)
    df = load_expenses(st.session_state.user)
    _, budget_percentage = budget_alert(df, user_budget)
    
    st.markdown(f"""
    <div style='background: rgba(102, 126, 234, 0.1); padding: 16px; border-radius: 12px; margin-bottom: 24px;'>
        <p style='margin: 0; color: #475569;'>
            💡 <b>Budget Status:</b> {budget_percentage:.1f}% used (₹{user_budget:,.0f} monthly budget)
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("📅 Expense Date", value=datetime.now())
            category = st.selectbox(
                "🏷️ Category",
                ["Food", "Travel", "Shopping", "Bills", "Health", "Entertainment", "Education", "Other"]
            )

        with col2:
            amount = st.number_input("💵 Amount (₹)", min_value=0.01, step=10.0)
            note = st.text_input("📝 Description", placeholder="e.g., Lunch at restaurant")

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button("✅ Add Expense", use_container_width=True)

        if submitted:
            result = save_expense(st.session_state.user, date, category, amount, note)
            
            if result:
                st.success("✅ Expense added successfully!")
                st.balloons()
                
                # Show updated budget status
                df = load_expenses(st.session_state.user)
                _, new_percentage = budget_alert(df, user_budget)
                
                if new_percentage > 90:
                    st.warning(f"⚠️ Warning: {new_percentage:.1f}% of monthly budget used!")
                
                st.rerun()
            else:
                st.error("❌ Failed to add expense")


# ================= ANALYTICS PAGE =================
elif page == "📈 Analytics":

    st.markdown("<h1>📈 Advanced Analytics Dashboard</h1>", unsafe_allow_html=True)

    df = load_expenses(st.session_state.user)

    if df.empty:
        st.warning("📊 No data available. Start adding expenses first!")
    else:
        summary = get_category_summary(df)
        user_budget = get_user_budget(st.session_state.user)

        # Top Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_spending = get_total_expenses(df)
        top_category = summary.idxmax()
        top_category_amount = summary.max()
        avg_transaction = total_spending / len(df)

        col1.metric("💰 Total Spending", f"₹{total_spending:,.2f}")
        col2.metric("🏆 Top Category", top_category)
        col3.metric("📊 Avg Transaction", f"₹{avg_transaction:,.2f}")
        col4.metric("📈 Total Entries", len(df))

        st.markdown("---")

        # Visualizations
        st.markdown("## 📊 Visual Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🥧 Category Distribution")
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            colors = sns.color_palette("husl", len(summary))
            ax1.pie(summary, labels=summary.index, autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)
            plt.close()

        with col2:
            st.subheader("📊 Spending by Category")
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            bars = ax2.bar(summary.index, summary.values, color=colors)
            ax2.set_ylabel('Amount (₹)', fontsize=12)
            ax2.set_xlabel('Category', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

        st.markdown("---")

        # Pattern Analysis
        patterns = analyze_spending_patterns(df)
        
        if patterns:
            st.markdown("## 🔍 Spending Pattern Analysis <span class='ml-badge'>ML</span>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📅 Weekday vs Weekend")
                if 'weekday_avg' in patterns and 'weekend_avg' in patterns:
                    st.metric("Weekday Average", f"₹{patterns['weekday_avg']:,.2f}")
                    st.metric("Weekend Average", f"₹{patterns['weekend_avg']:,.2f}")
                    
                    difference = patterns['weekend_avg'] - patterns['weekday_avg']
                    if difference > 0:
                        st.info(f"💡 You spend ₹{difference:,.2f} more on weekends on average")
                    else:
                        st.info(f"💡 You spend ₹{abs(difference):,.2f} less on weekends on average")
            
            with col2:
                st.markdown("### 🏷️ Category Insights")
                category_trends = patterns.get('category_trends', {})
                if category_trends and 'sum' in category_trends:
                    top_3_categories = sorted(
                        category_trends['sum'].items(), 
                        key=lambda x: x[1], 
                        reverse=True
                    )[:3]
                    
                    for idx, (cat, amount) in enumerate(top_3_categories, 1):
                        st.write(f"**{idx}. {cat}:** ₹{amount:,.2f}")


# ================= ML INSIGHTS PAGE =================
elif page == "🤖 ML Insights":

    st.markdown("<h1>🤖 Machine Learning Insights <span class='ml-badge'>Advanced ML</span></h1>", unsafe_allow_html=True)

    df = load_expenses(st.session_state.user)
    user_budget = get_user_budget(st.session_state.user)

    if df.empty:
        st.warning("🤖 Need data to generate ML insights. Add expenses first!")
    else:
        # Savings Potential
        st.markdown("## 💡 Savings Potential Analysis")
        savings_opportunities = calculate_savings_potential(df, user_budget)
        
        if savings_opportunities:
            for category, data in savings_opportunities.items():
                st.markdown(f"""
                <div class="feature-card" style="margin: 16px 0;">
                    <h3>🏷️ {category}</h3>
                    <p><b>Current Spending:</b> ₹{data['current']:,.2f} ({data['percentage']}% of total)</p>
                    <p><b>Potential Monthly Savings:</b> ₹{data['potential_savings']:,.2f}</p>
                    <p style="color: #667eea;"><b>💡 Suggestion:</b> {data['suggestion']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ No major savings opportunities detected. Your spending is well-balanced!")

        st.markdown("---")

        # Budget Recommendations
        st.markdown("## 🎯 AI-Recommended Category Budgets")
        recommendations = recommend_category_budgets(df, user_budget)
        
        if recommendations:
            st.markdown(f"""
            <div style='background: rgba(102, 126, 234, 0.1); padding: 16px; border-radius: 12px; margin-bottom: 16px;'>
                Based on your historical spending patterns, here's how we recommend allocating your 
                monthly budget of ₹{user_budget:,.0f}:
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            for idx, (category, recommended_amount) in enumerate(recommendations.items()):
                with col1 if idx % 2 == 0 else col2:
                    st.metric(f"🏷️ {category}", f"₹{recommended_amount:,.2f}")

        st.markdown("---")

        # Future Predictions
        st.markdown("## 🔮 Predictive Analytics")
        
        monthly_data, forecast, confidence = monthly_forecast(df)
        breach_prob, breach_msg = predict_budget_breach(df, user_budget)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📅 Next Month Forecast", f"₹{forecast if forecast else 0:,.2f}")
            if confidence:
                st.caption(f"95% Confidence: ₹{confidence[0]:,.0f} - ₹{confidence[1]:,.0f}")
        
        with col2:
            st.metric("⚠️ Budget Breach Risk", f"{breach_prob}%")
            st.caption(breach_msg)
        
        with col3:
            future = predict_future_expense(df)
            st.metric("🔮 Next Expense", f"₹{future if future else 0:,.2f}")
            st.caption("Based on spending patterns")

        st.markdown("---")

        # Anomaly Detection
        st.markdown("## 🚨 Anomaly Detection Results")
        anomalies = detect_spending_anomalies(df)
        
        if anomalies:
            st.warning(f"🔍 Detected {len(anomalies)} unusual transactions")
            
            anomaly_df = pd.DataFrame(anomalies)
            anomaly_df['Date'] = pd.to_datetime(anomaly_df['Date']).dt.strftime('%d %b %Y')
            anomaly_df['Amount'] = anomaly_df['Amount'].apply(lambda x: f"₹{x:,.2f}")
            
            st.dataframe(
                anomaly_df[['Date', 'Category', 'Amount', 'Note']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No anomalies detected. All expenses are within normal patterns.")


# ================= SETTINGS PAGE =================
elif page == "⚙️ Settings":

    st.markdown("<h1>⚙️ Account Settings</h1>", unsafe_allow_html=True)

    st.markdown("## 💰 Budget Configuration")
    
    current_budget = get_user_budget(st.session_state.user)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <h3>Current Monthly Budget</h3>
            <h2 style="color: #667eea;">₹{current_budget:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        new_budget = st.number_input(
            "Set New Monthly Budget (₹)",
            min_value=1000,
            value=int(current_budget),
            step=1000,
            key="settings_budget"
        )
        
        if st.button("💾 Update Budget", use_container_width=True, key="settings_update_btn"):
            if update_user_budget(st.session_state.user, new_budget):
                st.session_state.monthly_budget = new_budget
                st.success("✅ Budget updated successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to update budget")

    st.markdown("---")

    # Data Management
    st.markdown("## 📊 Data Management")
    
    df = load_expenses(st.session_state.user)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        if not df.empty:
            earliest = df['Date'].min().strftime('%d %b %Y')
            st.metric("Data Since", earliest)
        else:
            st.metric("Data Since", "No data")
    with col3:
        st.metric("Total Spending", f"₹{get_total_expenses(df):,.2f}")

    st.markdown("---")

    # About Section
    st.markdown("## ℹ️ About This Application")
    
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI Expense Intelligence Platform</h3>
        <p><b>Version:</b> 2.0 (ML-Enhanced)</p>
        <p><b>Features:</b></p>
        <ul>
            <li>🤖 Machine Learning Predictions (Linear Regression, Random Forest)</li>
            <li>📊 Statistical Anomaly Detection</li>
            <li>🎯 Smart Budget Management with Predictive Alerts</li>
            <li>📈 Advanced Pattern Analysis & Insights</li>
            <li>💡 AI-Powered Savings Recommendations</li>
            <li>🔮 Time Series Forecasting</li>
        </ul>
        <p><b>Tech Stack:</b> Python, Streamlit, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn</p>
    </div>
    """, unsafe_allow_html=True)


# ================= FOOTER =================
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #64748b; font-size: 14px;'>
    <p>🤖 <b>AI Expense Intelligence</b></p>
    <p>Powered by Machine Learning</p>
    <p style='font-size: 12px;'>Version 2.0 • ML-Enhanced</p>
</div>
""", unsafe_allow_html=True)
