from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -------------------------
# Demo Users (Role Based)
# -------------------------
USERS = {
    "student": {"password": "123", "role": "student"},
    "admin": {"password": "admin", "role": "admin"}
}


# -------------------------
# LOGIN PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("login.html")



# -------------------------
# LOGIN ACTION
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = USERS.get(username)

    if user and user["password"] == password:
        if user["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("student_dashboard"))

    return "Invalid credentials"


# -------------------------
# STUDENT DASHBOARD
# -------------------------
@app.route("/student")
def student_dashboard():
    return render_template("student_dashboard.html")


# -------------------------
# EXAM PAGE
# -------------------------
@app.route("/exam")
def exam():
    return render_template("exam.html")


# -------------------------
# EXAM SUBMIT → RESULT
# -------------------------
@app.route("/submit_exam", methods=["POST"])
def submit_exam():
    return render_template("result.html")


# -------------------------
# ADMIN DASHBOARD
# -------------------------
@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
