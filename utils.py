import pandas as pd
import os
from datetime import datetime

# Define the CSV file path
CSV_FILE = "expenses.csv"

def initialize_csv():
    """
    Initialize the CSV file with headers if it doesn't exist.
    This ensures the app works on first run.
    """
    if not os.path.exists(CSV_FILE):
        # Create DataFrame with column headers
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Note'])
        # Save to CSV
        df.to_csv(CSV_FILE, index=False)
        print(f"✅ Created new expense file: {CSV_FILE}")

def save_expense(date, category, amount, note):
    """
    Save a new expense to the CSV file.
    
    Parameters:
        date (datetime.date): Date of the expense
        category (str): Expense category
        amount (float): Expense amount
        note (str): Description/note about the expense
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create a dictionary for the new expense
        new_expense = {
            'Date': date.strftime('%Y-%m-%d'),
            'Category': category,
            'Amount': round(float(amount), 2),
            'Note': note.strip()
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_expense])
        
        # Append to existing CSV
        new_df.to_csv(CSV_FILE, mode='a', header=False, index=False)
        
        print(f"✅ Expense saved: {category} - Rs.{amount}")
        return True
    
    except Exception as e:
        print(f"❌ Error saving expense: {e}")
        return False

def load_expenses():
    """
    Load all expenses from the CSV file.
    
    Returns:
        pd.DataFrame: DataFrame containing all expenses
    """
    try:
        # Check if file exists and has data
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            
            # Convert Date column to datetime
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
            
            return df
        else:
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Note'])
    
    except Exception as e:
        print(f"❌ Error loading expenses: {e}")
        return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Note'])

def get_total_expenses(df):
    """
    Calculate the total of all expenses.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing expenses
    
    Returns:
        float: Total expense amount
    """
    if df.empty:
        return 0.0
    
    return round(df['Amount'].sum(), 2)

def get_category_summary(df):
    """
    Get total expenses grouped by category.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing expenses
    
    Returns:
        pd.Series: Series with category as index and total amount as values
    """
    if df.empty:
        return pd.Series(dtype=float)
    
    # Group by category and sum amounts
    category_totals = df.groupby('Category')['Amount'].sum()
    
    # Sort by amount in descending order
    category_totals = category_totals.sort_values(ascending=False)
    
    return category_totals

def get_expense_by_category(df, category):
    """
    Get all expenses for a specific category.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing expenses
        category (str): Category to filter by
    
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if df.empty:
        return df
    
    return df[df['Category'] == category]

def get_expenses_by_date_range(df, start_date, end_date):
    """
    Get expenses within a specific date range.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing expenses
        start_date (datetime): Start date
        end_date (datetime): End date
    
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if df.empty:
        return df
    
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter by date range
    mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
    
    return df[mask]

def get_monthly_summary(df):
    """
    Get expenses grouped by month.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing expenses
    
    Returns:
        pd.DataFrame: DataFrame with monthly totals
    """
    if df.empty:
        return pd.DataFrame(columns=['Month', 'Total'])
    
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract month-year
    df['Month'] = df['Date'].dt.to_period('M')
    
    # Group by month and sum
    monthly_totals = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_totals.columns = ['Month', 'Total']
    
    return monthly_totals

def delete_expense_by_index(index):
    """
    Delete an expense by its index (row number).
    
    Parameters:
        index (int): Row index to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df = load_expenses()
        
        if df.empty or index >= len(df):
            return False
        
        # Drop the row
        df = df.drop(index)
        
        # Save back to CSV
        df.to_csv(CSV_FILE, index=False)
        
        print(f"✅ Expense deleted at index {index}")
        return True
    
    except Exception as e:
        print(f"❌ Error deleting expense: {e}")
        return False

def get_statistics(df):
    """
    Calculate various statistics from expenses.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing expenses
    
    Returns:
        dict: Dictionary containing statistics
    """
    if df.empty:
        return {
            'total': 0,
            'average': 0,
            'max': 0,
            'min': 0,
            'count': 0
        }
    
    stats = {
        'total': round(df['Amount'].sum(), 2),
        'average': round(df['Amount'].mean(), 2),
        'max': round(df['Amount'].max(), 2),
        'min': round(df['Amount'].min(), 2),
        'count': len(df)
    }
    
    return stats