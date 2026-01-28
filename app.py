from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
    return render_template("result.html", score=score)

@app.route("/admin")
def admin():
    return render_template("admin_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
