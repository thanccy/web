from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# Home page: add form (Create) + table of records (Read)
HOME_PAGE = """
<h2>Students</h2>
<form method="POST">
  <input name="name" placeholder="Name" required>
  <input name="course" placeholder="Course" required>
  <button>Add</button>
</form>
<br>
<table border="1" cellpadding="6">
  <tr><th>ID</th><th>Name</th><th>Course</th><th>Actions</th></tr>
  {% for student in students %}
  <tr>
    <td>{{ student[0] }}</td>
    <td>{{ student[1] }}</td>
    <td>{{ student[2] }}</td>
    <td><a href="/edit/{{ student[0] }}">Edit</a> | <a href="/delete/{{ student[0] }}">Delete</a></td>
  </tr>
  {% endfor %}
</table>
"""

# Edit page: form filled with the old values (Update)
EDIT_PAGE = """
<h2>Edit Student</h2>
<form method="POST">
  <input name="name" value="{{ student[1] }}" required>
  <input name="course" value="{{ student[2] }}" required>
  <button>Save</button>
</form>
<a href="/">Cancel</a>
"""


# Runs one SQL command and returns all rows found (if any)
def run_query(sql, values=()):
    connection = sqlite3.connect("students.db")
    rows = connection.execute(sql, values).fetchall()
    connection.commit()
    connection.close()
    return rows


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":  # Create
        run_query("INSERT INTO students (name, course) VALUES (?, ?)",
                  (request.form["name"], request.form["course"]))
        return redirect("/")

    students = run_query("SELECT * FROM students")  # Read
    return render_template_string(HOME_PAGE, students=students)


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit(student_id):
    if request.method == "POST":  # Update
        run_query("UPDATE students SET name = ?, course = ? WHERE id = ?",
                  (request.form["name"], request.form["course"], student_id))
        return redirect("/")

    student = run_query("SELECT * FROM students WHERE id = ?", (student_id,))[0]
    return render_template_string(EDIT_PAGE, student=student)


@app.route("/delete/<int:student_id>")
def delete(student_id):  # Delete
    run_query("DELETE FROM students WHERE id = ?", (student_id,))
    return redirect("/")


if __name__ == "__main__":
    run_query("CREATE TABLE IF NOT EXISTS students "
              "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, course TEXT)")
    app.run(debug=True)
