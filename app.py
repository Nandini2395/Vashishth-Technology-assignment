from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Route: Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if login is valid
        if username == "professor" and password == "password123":  # Dummy credentials
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Route: Manage Students
@app.route("/manage-students", methods=["GET", "POST"])
def manage_students():
    conn = get_db_connection()
    if request.method == "POST":
        action = request.form["action"]
        name = request.form["name"]
        month = request.form["month"]

        if action == "add":
            conn.execute("INSERT INTO students (month_name, student_name, present_days, absent_days) VALUES (?, ?, 0, 0)", (month, name))
            conn.commit()
            flash(f"Student {name} added successfully!", "success")
        elif action == "remove":
            conn.execute("DELETE FROM students WHERE student_name = ?", (name,))
            conn.commit()
            flash(f"Student {name} removed successfully!", "warning")

    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("manage_students.html", students=students)

# Route: Div A Attendance
@app.route("/div-a-attendance", methods=["GET", "POST"])
def div_a_attendance():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students WHERE month_name = 'January'").fetchall()
    conn.close()
    return render_template("div_a_attendance.html", students=students)

# Route: Div B Attendance
@app.route("/div-b-attendance", methods=["GET", "POST"])
def div_b_attendance():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students WHERE month_name = 'February'").fetchall()
    conn.close()
    return render_template("div_b_attendance.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
