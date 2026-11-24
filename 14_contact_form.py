from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# The HTML page (form + confirmation message)
PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Contact Form</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 400px; margin: 20px auto; }
    input, textarea { display: block; width: 100%; padding: 8px; margin-bottom: 10px; box-sizing: border-box; }
    .success { color: green; }
  </style>
</head>
<body>
  <h2>Contact Us</h2>

  {% if confirmation %}
    <p class="success">{{ confirmation }}</p>
  {% endif %}

  <form method="POST">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="email" name="email" placeholder="Your email" required>
    <textarea name="message" placeholder="Your message" rows="4" required></textarea>
    <button type="submit">Send</button>
  </form>
</body>
</html>
"""


# Create the database table if it does not exist
def create_table():
    connection = sqlite3.connect("contacts.db")
    connection.execute(
        "CREATE TABLE IF NOT EXISTS contacts "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)"
    )
    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def contact():
    confirmation = ""

    # Runs only when the form is submitted
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Save the data in the database
        connection = sqlite3.connect("contacts.db")
        connection.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message),
        )
        connection.commit()
        connection.close()

        confirmation = "Thank you, " + name + "! Your message has been sent."

    return render_template_string(PAGE, confirmation=confirmation)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
