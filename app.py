import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db():
    return sqlite3.connect("exam.db")

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER
    )
    """)

    db.commit()
    db.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        if role == "student":
            return redirect("/student")
        else:
            return redirect("/admin")
    return render_template("login.html")

@app.route("/student")
def student():
    return render_template("student_dashboard.html")

@app.route("/exam")
def exam():
    return render_template("exam.html")

@app.route("/submit", methods=["POST"])
def submit():
    score = 0
    if request.form.get("q1") == "b":
        score += 1
    if request.form.get("q2") == "a":
        score += 1

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO results (score) VALUES (?)", (score,))
    db.commit()
    db.close()

    return render_template("result.html", score=score)


@app.route("/admin")
def admin():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM results")
    data = cursor.fetchall()
    db.close()

    return render_template("admin_dashboard.html", data=data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

