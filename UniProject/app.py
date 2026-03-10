from flask import Flask, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue

from UniProject.models.users.users import get_user_role, init_db, register_user, verify_user
from UniProject.services.api_service import call_api

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


@app.route("/", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    """
    Handle user login. Render the login page and process login form submissions.

    Returns:
        ResponseReturnValue: Rendered HTML for the login page or redirects to track on success.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password and verify_user(username, password):
            session["username"] = username
            return redirect(url_for("track"))
        else:
            error = "Invalid username or password."
            return render_template("index.html", error=error)
    return render_template("index.html")


@app.route("/track", methods=["GET", "POST"])
def track() -> ResponseReturnValue:
    """
    Render the track page and handle API call form submissions.

    Returns:
        ResponseReturnValue: Rendered HTML for the track page.
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
        "track.html", name=session.get("username", "Guest"), companyName="MyCompany", api_result=api_result
    )


@app.route("/process", methods=["GET", "POST"])
def process() -> ResponseReturnValue:
    """
    Render the process page and handle API call form submissions.

    Returns:
        ResponseReturnValue: Rendered HTML for the process page.
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
    return render_template("process.html", name=session.get("username"), companyName="MyCompany", api_result=api_result)


@app.route("/report", methods=["GET", "POST"])
def report() -> ResponseReturnValue:
    """
    Render the report page and handle API call form submissions.

    Returns:
        ResponseReturnValue: Rendered HTML for the report page.
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
    return render_template("report.html", name=session.get("username"), companyName="MyCompany", api_result=api_result)


@app.route("/register", methods=["GET", "POST"])
def register() -> ResponseReturnValue:
    """
    Render the user registration page and handle registration form submissions.
    Only accessible by admin users.

    Returns:
        ResponseReturnValue: Rendered HTML for the registration page or redirects to track on success.
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
                return redirect(url_for("track"))
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
