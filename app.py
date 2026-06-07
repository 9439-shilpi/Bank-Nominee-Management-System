from flask import Flask, render_template, request, redirect
import json
import os
import mysql.connector

app = Flask(__name__)

FILE = "data.json"

# ---------------- MYSQL CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

# ---------------- CREATE JSON FILE ----------------
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ADD Jatin/Sunandana ----------------
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

    try:
         # Feature added by Sunandana Sahoo:
        # STEP 1: Only one Primary allowed
        if nominee_type == "Primary":
            cursor.execute("SELECT name FROM nominees WHERE nominee_type='Primary'")
            existing_primary = cursor.fetchone()

            if existing_primary:
                return f"❌ {existing_primary[0]} is already Primary nominee. Only one Primary is allowed."

        # Feature added by Jatin Bhangotra:
        # STEP 2: Maximum 2 Secondary nominees allowed
        if nominee_type == "Secondary":
            cursor.execute("SELECT COUNT(*) FROM nominees WHERE nominee_type='Secondary'")
            secondary_count = cursor.fetchone()[0]
            
            if secondary_count >= 2:
                return "❌ Only 2 Secondary nominees are allowed."

        # Feature added by Jatin Bhangotra:    
        # STEP 3: Account number must be unique
        cursor.execute("SELECT account FROM nominees WHERE account=%s", (account,))
        existing_account = cursor.fetchone()

        if existing_account:
            return "❌ Account number already exists."

        # STEP 4: Insert nominee
        cursor.execute("""
            INSERT INTO nominees (name, gender, relation, account, share_percentage, nominee_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, gender, relation, account, share_percentage, nominee_type))

        conn.commit()

        return redirect("/view")

    finally:
        cursor.close()
        conn.close()

# ---------------- VIEW by Jatin Bhangotra----------------
@app.route("/view")
def view():

    search = request.args.get("search")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Feature added by Jatin Bhangotra:
    # Search nominees by name or account number
    if search:
        cursor.execute("""
            SELECT * FROM nominees
            WHERE name LIKE %s OR account LIKE %s
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM nominees")

    nominees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view.html", nominees=nominees)

# ---------------- UPDATE  by Sunandana Sahoo----------------
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

# ---------------- DELETE by Sunandana Sahoo----------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM nominees WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/view")

# ---------------- API by Jatin Bhangotra ----------------
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

# ---------------- DASHBOARD----------------
@app.route("/dashboard")
def dashboard():
    with open(FILE, "r") as f:
        data = json.load(f)

    return render_template("dashboard.html", total=len(data))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5007)