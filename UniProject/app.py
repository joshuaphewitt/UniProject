import sqlite3
from typing import Dict, Optional

import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


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


def call_api(
    url: str, headers: Optional[Dict[str, str]] = None, method: str = "GET"
) -> str:
    """
    Call an external API using the specified URL, headers, and HTTP method.

    Args:
        url (str): The API endpoint URL.
        headers (Optional[Dict[str, str]]): Optional HTTP headers to include in the request.
        method (str): HTTP method to use ("GET" or "POST"). Defaults to "GET".

    Returns:
        str: The response text from the API, or an error message on failure.
    """
    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        return response.text
    except Exception as exception:
        return f"Error: {exception}"


def list_ftp(
    url: str, port: int, username: str, password: str, dir: str
) -> Optional[str]:
    """
    Docstring for list_ftp

    :param url: Description
    :type url: str
    :param port: Description
    :type port: int
    :param username: Description
    :type username: str
    :param password: Description
    :type password: str
    :param dir: Description
    :type dir: str
    """
    return None


@app.route("/", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    """
    Handle user login. Render the login page and process login form submissions.

    Returns:
        ResponseReturnValue: Rendered HTML for the login page or redirects to dashboard on success.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password and verify_user(username, password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
            return render_template("index.html", error=error)
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard() -> ResponseReturnValue:
    """
    Render the dashboard page and handle API call form submissions.

    Returns:
        ResponseReturnValue: Rendered HTML for the dashboard page.
    """
    if "username" not in session:
        return redirect(url_for("login"))
    api_result = None
    if request.method == "POST":
        url = request.form.get("url")
        method = request.form.get("method", "GET")

        headers = {}
        for key in request.form:
            if key.startswith("header_name_"):
                index = key.split("_")[-1]
                name = request.form.get(f"header_name_{index}")
                value = request.form.get(f"header_value_{index}")
                if name:
                    headers[name] = value or ""

        if url:
            api_result = call_api(url, headers=headers, method=method)
    return render_template(
        "dashboard.html", name=session["username"], api_result=api_result
    )


@app.route("/register", methods=["GET", "POST"])
def register() -> ResponseReturnValue:
    """
    Render the user registration page and handle registration form submissions.
    Only accessible by admin users.

    Returns:
        ResponseReturnValue: Rendered HTML for the registration page or redirects to dashboard on success.
    """
    if "username" not in session or get_user_role(session["username"]) != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        role = request.form.get("role", "user")
        if username and password and name:
            success = register_user(username, password, name, role)
            if success:
                return redirect(url_for("dashboard"))
            else:
                error = "Username already exists."
                return render_template("register.html", error=error)
        else:
            error = "Please provide username, password, and name."
            return render_template("register.html", error=error)
    return render_template("register.html")


@app.route("/logout")
def logout() -> ResponseReturnValue:
    """
    Log out the current user and redirect to the login page.

    Returns:
        ResponseReturnValue: Redirect response to the login page.
    """
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    """
    Entry point for running the Flask application.
    Initializes the database and starts the server.
    """
    init_db()
    app.run(debug=True)
