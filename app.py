import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from utils import (
    initialize_csv,
    save_expense,
    load_expenses,
    get_total_expenses,
    get_category_summary,
    get_expense_by_category 
)

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    [data-testid="stMetric"] {
        background-color: #le293b;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #60a5fa;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize CSV file on first run
initialize_csv()

# Sidebar Navigation
st.sidebar.title("📊 Navigation Menu")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select a Page:",
    ["🏠 Dashboard", "➕ Add Expense", "📈 Analytics"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("💡 *Tip:* Track your expenses daily for better financial insights!")

# ========== PAGE 1: DASHBOARD ==========
if page == "🏠 Dashboard":
    st.title("💰 Personal Expense Tracker Dashboard")
    st.markdown("### Welcome to your expense management system")
    
    # Load expenses data
    df = load_expenses()
    
    if df.empty:
        st.warning("⚠️ No expenses recorded yet. Go to 'Add Expense' to get started!")
    else:
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total = get_total_expenses(df)
            st.metric("💵 Total Expenses", f"Rs.{total:,.2f}")
        
        with col2:
            num_transactions = len(df)
            st.metric("📝 Total Transactions", num_transactions)
        
        with col3:
            avg_expense = total / num_transactions if num_transactions > 0 else 0
            st.metric("📊 Average Expense", f"Rs.{avg_expense:,.2f}")
        
        st.markdown("---")
        
        # Display expense table
        st.subheader("📋 Recent Expenses")
        
        # Format the dataframe for display
        display_df = df.copy()
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"Rs.{x:,.2f}")
        display_df = display_df.sort_values('Date', ascending=False)
        
        # Display with custom styling
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Option to download data
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Expense Data as CSV",
            data=csv,
            file_name=f"expenses_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

# ========== PAGE 2: ADD EXPENSE ==========
elif page == "➕ Add Expense":
    st.title("➕ Add New Expense")
    st.markdown("### Fill in the details below to record your expense")
    
    # Create form for expense entry
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Date input
            date = st.date_input(
                "📅 Date",
                value=datetime.now(),
                help="Select the date of the expense"
            )
            
            # Category dropdown
            category = st.selectbox(
                "🏷️ Category",
                ["Food", "Travel", "Shopping", "Bills", "Health", "Other"],
                help="Choose the expense category"
            )
        
        with col2:
            # Amount input
            amount = st.number_input(
                "💵 Amount (Rs.)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                help="Enter the expense amount"
            )
            
            # Note input
            note = st.text_input(
                "📝 Note",
                placeholder="e.g., Lunch at restaurant",
                help="Add a brief description"
            )
        
        # Submit button
        submitted = st.form_submit_button("✅ Add Expense", use_container_width=True)
        
        if submitted:
            # Validate inputs
            if amount <= 0:
                st.error("❌ Please enter a valid amount greater than 0!")
            elif not note.strip():
                st.error("❌ Please add a note describing the expense!")
            else:
                # Save expense to CSV
                success = save_expense(date, category, amount, note)
                
                if success:
                    st.success(f"✅ Expense of Rs.{amount:.2f} added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to save expense. Please try again.")
    
    # Display recent expenses summary
    st.markdown("---")
    st.subheader("📊 Recent Expense Summary")
    
    df = load_expenses()
    if not df.empty:
        # Show last 5 expenses
        recent_df = df.tail(5).sort_values('Date', ascending=False)
        
        for idx, row in recent_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
                with col1:
                    st.write(f"📅 {row['Date']}")
                with col2:
                    st.write(f"🏷️ {row['Category']}")
                with col3:
                    st.write(f"💵 Rs.{row['Amount']:.2f}")
                with col4:
                    st.write(f"📝 {row['Note']}")
                st.markdown("---")

# ========== PAGE 3: ANALYTICS ==========
elif page == "📈 Analytics":
    st.title("📈 Expense Analytics")
    st.markdown("### Visualize your spending patterns")
    
    # Load expenses data
    df = load_expenses()
    
    if df.empty:
        st.warning("⚠️ No data available for analytics. Add some expenses first!")
    else:
        # Get category summary
        category_summary = get_category_summary(df)
        
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💰 Total Spending", f"Rs.{get_total_expenses(df):,.2f}")
        
        with col2:
            most_spent_category = category_summary.idxmax()
            st.metric("🏆 Highest Spending Category", most_spent_category)
        
        st.markdown("---")
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # PIE CHART - Category Distribution
            st.subheader("🥧 Spending Distribution by Category")
            
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
            
            wedges, texts, autotexts = ax1.pie(
                category_summary,
                labels=category_summary.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                explode=[0.05] * len(category_summary)
            )
            
            # Improve text readability
            for text in texts:
                text.set_fontsize(10)
                text.set_weight('bold')
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_weight('bold')
            
            ax1.axis('equal')
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col2:
            # BAR CHART - Category vs Amount
            st.subheader("📊 Spending by Category")
            
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            
            bars = ax2.bar(
                category_summary.index,
                category_summary.values,
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
                edgecolor='black',
                linewidth=1.2
            )
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height,
                    f'Rs.{height:,.0f}',
                    ha='center',
                    va='bottom',
                    fontsize=9,
                    weight='bold'
                )
            
            ax2.set_xlabel('Category', fontsize=11, weight='bold')
            ax2.set_ylabel('Amount (Rs.)', fontsize=11, weight='bold')
            ax2.set_title('Total Spending per Category', fontsize=12, weight='bold')
            ax2.grid(axis='y', alpha=0.3, linestyle='--')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)
        
        st.markdown("---")
        
        # Category breakdown table
        st.subheader("📋 Detailed Category Breakdown")
        
        breakdown_df = pd.DataFrame({
            'Category': category_summary.index,
            'Total Amount': category_summary.values,
            'Percentage': (category_summary.values / category_summary.sum() * 100).round(2)
        })
        
        breakdown_df['Total Amount'] = breakdown_df['Total Amount'].apply(lambda x: f"Rs.{x:,.2f}")
        breakdown_df['Percentage'] = breakdown_df['Percentage'].apply(lambda x: f"{x}%")
        
        st.dataframe(
            breakdown_df,
            use_container_width=True,
            hide_index=True
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 About")
st.sidebar.info("""
*Personal Expense Tracker v1.0*  
Built with ❤️ using Streamlit  
© 2025 | Track Smart, Save Smart
""")