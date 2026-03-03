import sqlite3
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash


def init_db() -> None:
    """
    Initialize the SQLite database and create the users table if it does not exist.

    Returns:
        None
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  name TEXT NOT NULL,
                  role TEXT NOT NULL DEFAULT 'user')""")
    conn.commit()
    conn.close()


def create_superuser(username: str, password: str, name: str) -> bool:
    """
    Create a new superuser (admin) in the database.

    Args:
        username (str): The username for the new superuser.
        password (str): The password for the new superuser.
        name (str): The display name for the new superuser.

    Returns:
        bool: True if creation was successful, False if username already exists.
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        c.execute(
            "INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
            (username, hashed_password, name, "admin"),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def register_user(username: str, password: str, name: str, role: str = "user") -> bool:
    """
    Register a new user in the database.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        name (str): The display name for the new user.
        role (str, optional): The role for the new user. Defaults to "user".

    Returns:
        bool: True if registration was successful, False if username already exists.
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        c.execute(
            "INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
            (username, hashed_password, name, role),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    """
    Verify if the provided username and password match a user in the database.

    Args:
        username (str): The username to check.
        password (str): The password to verify.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False


def get_user_role(username: str) -> Optional[str]:
    """
    Get the role of the specified user.

    Args:
        username (str): The username to look up.

    Returns:
        Optional[str]: The role of the user, or None if not found.
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return str(row[0])
    return None
