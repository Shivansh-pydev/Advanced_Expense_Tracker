import sqlite3
import hashlib

# ================= DATABASE FILE =================
DB = "users.db"


# ================= CONNECT DATABASE =================
def connect():
    """
    Create database connection.
    check_same_thread=False is required for Streamlit reruns.
    """
    return sqlite3.connect(DB, check_same_thread=False)


# ================= CREATE USERS TABLE =================
def create_users_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


# ================= HASH PASSWORD =================
def hash_pass(password):
    """
    Securely hash password using SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ================= REGISTER USER =================
def register_user(username, password):
    """
    Create new user account.
    Returns True if success, False if user exists.
    """
    try:
        conn = connect()
        c = conn.cursor()

        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, hash_pass(password))
        )

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Register Error:", e)
        return False


# ================= LOGIN USER =================
def login_user(username, password):
    """
    Verify login credentials.
    Returns user row if valid, else None.
    """

    conn = connect()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_pass(password))
    )

    user = c.fetchone()
    conn.close()

    return user
