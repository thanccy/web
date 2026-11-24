from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# Home page: search form, add form, and table of employees
HOME_PAGE = """
<h2>Employee Management</h2>

<form method="GET">
  <input name="search" placeholder="Search by name or ID" value="{{ search }}">
  <button>Search</button>
  <a href="/">Show all</a>
</form>
<br>

<form method="POST">
  <input name="name" placeholder="Name" required>
  <input name="department" placeholder="Department" required>
  <input name="salary" type="number" placeholder="Salary" required>
  <button>Add Employee</button>
</form>
<br>

<table border="1" cellpadding="6">
  <tr><th>ID</th><th>Name</th><th>Department</th><th>Salary</th><th>Actions</th></tr>
  {% for employee in employees %}
  <tr>
    <td>{{ employee[0] }}</td>
    <td>{{ employee[1] }}</td>
    <td>{{ employee[2] }}</td>
    <td>{{ employee[3] }}</td>
    <td><a href="/edit/{{ employee[0] }}">Edit</a> | <a href="/delete/{{ employee[0] }}">Delete</a></td>
  </tr>
  {% endfor %}
</table>
{% if not employees %}<p>No employees found.</p>{% endif %}
"""

# Edit page: form filled with the old values
EDIT_PAGE = """
<h2>Edit Employee</h2>
<form method="POST">
  <input name="name" value="{{ employee[1] }}" required>
  <input name="department" value="{{ employee[2] }}" required>
  <input name="salary" type="number" value="{{ employee[3] }}" required>
  <button>Save</button>
</form>
<a href="/">Cancel</a>
"""


# Runs one SQL command and returns all rows found (if any)
def run_query(sql, values=()):
    connection = sqlite3.connect("employees.db")
    rows = connection.execute(sql, values).fetchall()
    connection.commit()
    connection.close()
    return rows


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":  # Add
        run_query("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
                  (request.form["name"], request.form["department"], request.form["salary"]))
        return redirect("/")

    # Search by name (partial match) or by ID. An empty search shows everyone.
    search = request.args.get("search", "").strip()
    employees = run_query("SELECT * FROM employees WHERE name LIKE ? OR id = ?",
                          ("%" + search + "%", search))
    return render_template_string(HOME_PAGE, employees=employees, search=search)


@app.route("/edit/<int:employee_id>", methods=["GET", "POST"])
def edit(employee_id):
    if request.method == "POST":  # Update
        run_query("UPDATE employees SET name = ?, department = ?, salary = ? WHERE id = ?",
                  (request.form["name"], request.form["department"], request.form["salary"], employee_id))
        return redirect("/")

    employee = run_query("SELECT * FROM employees WHERE id = ?", (employee_id,))[0]
    return render_template_string(EDIT_PAGE, employee=employee)


@app.route("/delete/<int:employee_id>")
def delete(employee_id):  # Delete
    run_query("DELETE FROM employees WHERE id = ?", (employee_id,))
    return redirect("/")


if __name__ == "__main__":
    run_query("CREATE TABLE IF NOT EXISTS employees "
              "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, department TEXT, salary INTEGER)")
    app.run(debug=True)
