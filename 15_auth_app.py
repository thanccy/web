from flask import Flask, request, session, redirect, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-secret"  # needed for sessions

# One page used for both Register and Login
FORM_PAGE = """
<style>
  body { font-family: Arial; max-width: 350px; margin: 20px auto; }
  input { display: block; width: 100%; padding: 8px; margin-bottom: 10px; box-sizing: border-box; }
</style>
<h2>{{ title }}</h2>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
<form method="POST">
  <input type="text" name="username" placeholder="Username" required>
  <input type="password" name="password" placeholder="Password" required>
  <button type="submit">{{ title }}</button>
</form>
<p><a href="{{ link_url }}">{{ link_text }}</a></p>
"""

DASHBOARD_PAGE = """
<h2>Welcome, {{ username }}!</h2>
<p>You are logged in.</p>
<a href="/logout">Logout</a>
"""


# Runs one SQL command and returns the first row found (if any)
def run_query(sql, values=()):
    connection = sqlite3.connect("users.db")
    row = connection.execute(sql, values).fetchone()
    connection.commit()
    connection.close()
    return row


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # Validation
        if username == "" or password == "":
            error = "All fields are required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif run_query("SELECT id FROM users WHERE username = ?", (username,)):
            error = "Username already taken."
        else:
            # Save a hashed password (never the plain password)
            run_query("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, generate_password_hash(password)))
            return redirect("/login")

    return render_template_string(FORM_PAGE, title="Register", error=error,
                                  link_text="Already have an account? Login", link_url="/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = run_query("SELECT password FROM users WHERE username = ?", (username,))

        # Compare the typed password with the stored hash
        if user and check_password_hash(user[0], password):
            session["username"] = username  # remember the user
            return redirect("/dashboard")
        error = "Invalid username or password."

    return render_template_string(FORM_PAGE, title="Login", error=error,
                                  link_text="New user? Register", link_url="/register")


@app.route("/dashboard")
def dashboard():
    # Only logged-in users can see this page
    if "username" not in session:
        return redirect("/login")
    return render_template_string(DASHBOARD_PAGE, username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    run_query("CREATE TABLE IF NOT EXISTS users "
              "(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
    app.run(debug=True)
