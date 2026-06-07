from flask import Flask, render_template, request, redirect
import json
import os
import mysql.connector

app = Flask(__name__)

FILE = "data.json"

# ---------------- MYSQL CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="NewPassword@123",
        database="bank_nominee_db"
    )

# ---------------- CREATE JSON FILE ----------------
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ADD ----------------
@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    gender = request.form["gender"]
    relation = request.form["relation"]
    account = request.form["account"]
    share_percentage = request.form["share_percentage"]
    nominee_type = request.form["nominee_type"]

    conn = get_connection()
    cursor = conn.cursor()

    # STEP 1: Only one Primary allowed
    if nominee_type == "Primary":
        cursor.execute("SELECT name FROM nominees WHERE nominee_type='Primary'")
        existing = cursor.fetchone()

        if existing:
            return f"❌ {existing[0]} is already Primary nominee. Only one Primary is allowed."

    # STEP 2: Insert nominee
    cursor.execute("""
        INSERT INTO nominees (name, gender, relation, account, share_percentage, nominee_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, gender, relation, account, share_percentage, nominee_type))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/view")
    

# ---------------- VIEW ----------------
@app.route("/view")
def view():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM nominees")
    nominees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view.html", nominees=nominees)

# ---------------- VIEW ----------------
@app.route("/edit/<int:id>")
def edit(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM nominees WHERE id=%s", (id,))
    nominee = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit.html", nominee=nominee)

# ---------------- UPDATE ----------------
@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    name = request.form["name"]
    gender = request.form["gender"]
    relation = request.form["relation"]
    account = request.form["account"]
    share_percentage = request.form["share_percentage"]
    nominee_type = request.form["nominee_type"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE nominees
        SET name=%s,
            gender=%s,
            relation=%s,
            account=%s,
            share_percentage=%s,
            nominee_type=%s
        WHERE id=%s
    """, (
        name,
        gender,
        relation,
        account,
        share_percentage,
        nominee_type,
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/view")

# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM nominees WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/view")

# ---------------- API ----------------
@app.route("/api/nominees")
def api_nominees():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, gender, relation,
               account, share_percentage, nominee_type
        FROM nominees
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"nominees": data}

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    with open(FILE, "r") as f:
        data = json.load(f)

    return render_template("dashboard.html", total=len(data))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5007)