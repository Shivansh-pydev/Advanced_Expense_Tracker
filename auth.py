import sqlite3
import hashlib
import os

# ================= DATABASE FILE =================
DB = "users.db"


# ================= CONNECT DATABASE =================
def connect():
    """
    Create database connection with proper settings.
    """
    conn = sqlite3.connect(DB, check_same_thread=False, timeout=10)
    return conn


# ================= CREATE USERS TABLE =================
def create_users_table():
    """
    Initialize users table with budget preferences.
    Handles existing table gracefully.
    """
    try:
        conn = connect()
        c = conn.cursor()

        # Check if table exists and has correct schema
        c.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        existing_table = c.fetchone()
        
        if existing_table is None:
            # Create new table
            c.execute("""
                CREATE TABLE users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    monthly_budget REAL DEFAULT 10000,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Users table created successfully")
        else:
            # Check if monthly_budget column exists
            c.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in c.fetchall()]
            
            if 'monthly_budget' not in columns:
                # Add missing column to existing table
                c.execute("ALTER TABLE users ADD COLUMN monthly_budget REAL DEFAULT 10000")
                conn.commit()
                print("✅ Updated users table with monthly_budget column")

        conn.close()
        
    except Exception as e:
        print("❌ Create Table Error:", e)


# ================= HASH PASSWORD =================
def hash_pass(password):
    """
    Securely hash password using SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ================= REGISTER USER =================
def register_user(username, password, monthly_budget=10000):
    """
    Create new user account with budget preference.
    Returns True if success, False if user exists or error.
    """
    if not username or not password:
        print("❌ Empty username or password")
        return False
    
    # Clean username (remove spaces, lowercase)
    username = username.strip().lower()
    
    if len(username) < 3:
        print("❌ Username too short")
        return False
    
    conn = None
    try:
        conn = connect()
        c = conn.cursor()

        # Check if user already exists (case-insensitive)
        c.execute("SELECT username FROM users WHERE LOWER(username)=?", (username,))
        existing = c.fetchone()
        
        if existing:
            print(f"❌ User '{username}' already exists")
            conn.close()
            return False

        # Insert new user
        hashed_pw = hash_pass(password)
        
        c.execute(
            "INSERT INTO users(username, password, monthly_budget) VALUES(?, ?, ?)",
            (username, hashed_pw, float(monthly_budget))
        )

        conn.commit()
        
        # Verify insertion
        c.execute("SELECT id, username FROM users WHERE username=?", (username,))
        result = c.fetchone()
        
        conn.close()
        
        if result:
            print(f"✅ User '{username}' registered successfully with ID: {result[0]}")
            return True
        else:
            print("❌ Registration verification failed")
            return False

    except sqlite3.IntegrityError as e:
        print(f"❌ Database Integrity Error: {e}")
        if conn:
            conn.close()
        return False
        
    except Exception as e:
        print(f"❌ Register Error: {e}")
        if conn:
            conn.close()
        return False


# ================= LOGIN USER =================
def login_user(username, password):
    """
    Verify login credentials and return user data.
    Returns tuple (id, username, monthly_budget) if valid, else None.
    """
    if not username or not password:
        return None
    
    # Clean username (case-insensitive)
    username = username.strip().lower()
    
    conn = None
    try:
        conn = connect()
        c = conn.cursor()

        hashed_password = hash_pass(password)
        
        c.execute(
            "SELECT id, username, monthly_budget FROM users WHERE LOWER(username)=? AND password=?",
            (username, hashed_password)
        )

        user = c.fetchone()
        conn.close()

        if user:
            print(f"✅ Login successful for user: {user[1]}")
        else:
            print(f"❌ Login failed for username: {username}")
        
        return user

    except Exception as e:
        print(f"❌ Login Error: {e}")
        if conn:
            conn.close()
        return None


# ================= GET USER BUDGET =================
def get_user_budget(username):
    """
    Retrieve user's monthly budget setting.
    """
    if not username:
        return 10000
    
    username = username.strip().lower()
    
    try:
        conn = connect()
        c = conn.cursor()
        c.execute("SELECT monthly_budget FROM users WHERE LOWER(username)=?", (username,))
        result = c.fetchone()
        conn.close()
        
        if result and result[0] is not None:
            return float(result[0])
        else:
            return 10000
            
    except Exception as e:
        print(f"❌ Get Budget Error: {e}")
        return 10000


# ================= UPDATE USER BUDGET =================
def update_user_budget(username, new_budget):
    """
    Update user's monthly budget setting.
    """
    if not username:
        return False
    
    username = username.strip().lower()
    
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(
            "UPDATE users SET monthly_budget=? WHERE LOWER(username)=?",
            (float(new_budget), username)
        )
        conn.commit()
        
        # Verify update
        c.execute("SELECT monthly_budget FROM users WHERE LOWER(username)=?", (username,))
        result = c.fetchone()
        
        conn.close()
        
        if result:
            print(f"✅ Budget updated to ₹{result[0]} for user: {username}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Update Budget Error: {e}")
        return False


# ================= VERIFY DATABASE =================
def verify_database():
    """
    Check database integrity and show all users.
    Returns list of tuples (username, monthly_budget).
    """
    try:
        conn = connect()
        c = conn.cursor()
        c.execute("SELECT username, monthly_budget FROM users ORDER BY created_at DESC")
        users = c.fetchall()
        conn.close()
        
        print(f"📊 Total users in database: {len(users)}")
        for user in users:
            print(f"  • {user[0]} (Budget: ₹{user[1]})")
        
        return users
        
    except Exception as e:
        print(f"❌ Database Verify Error: {e}")
        return []


# ================= DELETE USER (FOR TESTING) =================
def delete_user(username):
    """
    Delete a user from database (for testing/cleanup).
    """
    if not username:
        return False
    
    username = username.strip().lower()
    
    try:
        conn = connect()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE LOWER(username)=?", (username,))
        conn.commit()
        deleted_count = c.rowcount
        conn.close()
        
        if deleted_count > 0:
            print(f"✅ User '{username}' deleted successfully")
            return True
        else:
            print(f"❌ User '{username}' not found")
            return False
            
    except Exception as e:
        print(f"❌ Delete User Error: {e}")
        return False


# ================= RESET DATABASE (FOR TESTING) =================
def reset_database():
    """
    Clear all users from database (for testing).
    USE WITH CAUTION!
    """
    try:
        conn = connect()
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()
        deleted_count = c.rowcount
        conn.close()
        
        print(f"✅ Database reset: {deleted_count} users deleted")
        return True
        
    except Exception as e:
        print(f"❌ Reset Database Error: {e}")
        return False
