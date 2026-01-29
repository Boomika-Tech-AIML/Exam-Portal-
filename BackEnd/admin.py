from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "exam_portal_secret"

# -------------------------
# Dummy data (for demo)
# -------------------------
USERS = {
    "student1": "1234",
    "admin": "admin"
}

EXAM_DATA = {
    "title": "NAT Test",
    "question": "What is the capital of India?",
    "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
    "answer": "Delhi"
}

ADMIN_LOGS = []


# -------------------------
# Login
# -------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["user"] = username

            if username == "admin":
                return redirect(url_for("admin"))
            else:
                ADMIN_LOGS.append("[SUCCESS] User verified")
                return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# -------------------------
# Student Dashboard
# -------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=session["user"])


# -------------------------
# Exam Page
# -------------------------
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        selected = request.form.get("option")
        score = 0

        if selected == EXAM_DATA["answer"]:
            score = 100

        session["score"] = score
        ADMIN_LOGS.append(f"[SUBMITTED] {EXAM_DATA['title']} – {score}%")
        return redirect(url_for("result"))

    return render_template("exam.html", exam=EXAM_DATA)


# -------------------------
# Result Page
# -------------------------
@app.route("/result")
def result():
    if "user" not in session:
        return redirect(url_for("login"))

    score = session.get("score", 0)
    return render_template("result.html", score=score)


# -------------------------
# Admin Dashboard
# -------------------------
@app.route("/admin")
def admin():
    live_users = 1 if "user" in session else 0
    integrity_alerts = len([log for log in ADMIN_LOGS if "WARNING" in log])

    return render_template(
        "admin.html",
        live_users=live_users,
        alerts=integrity_alerts,
        avg_score=81,
        logs=ADMIN_LOGS
    )


# -------------------------
# Logout
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
