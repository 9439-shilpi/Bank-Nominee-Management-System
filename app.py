from flask import Flask, render_template, request, redirect
import json
import os
import mysql.connector

app = Flask(__name__)

FILE = "data.json"

# ---------------- MYSQL CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 25861))
    )
# ---------------- CREATE TABLE ----------------

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nominees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        gender VARCHAR(20),
        relation VARCHAR(100),
        account VARCHAR(100) UNIQUE,
        share_percentage VARCHAR(10),
        nominee_type VARCHAR(50)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

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

    conn = get_connection()
    cursor = conn.cursor()

    try:
        name = request.form["name"]
        gender = request.form["gender"]
        relation = request.form["relation"]
        account = request.form["account"]
        share_percentage = request.form["share_percentage"].replace("%", "")
        share_percentage = float(share_percentage)
        nominee_type = request.form["nominee_type"]

        # ✅ validation
        if not account.isdigit():
            return "❌ Account must contain only numbers"

        # Primary check
        if nominee_type == "Primary":
            cursor.execute("SELECT id FROM nominees WHERE nominee_type='Primary'")
            if cursor.fetchone():
                return "❌ Primary already exists"

        # Secondary limit
        if nominee_type == "Secondary":
            cursor.execute("SELECT COUNT(*) FROM nominees WHERE nominee_type='Secondary'")
            if cursor.fetchone()[0] >= 2:
                return "❌ Only 2 Secondary allowed"

        # Duplicate account
        cursor.execute("SELECT id FROM nominees WHERE account=%s", (account,))
        if cursor.fetchone():
            return "❌ Account already exists"

        # insert
        cursor.execute("""
            INSERT INTO nominees (name, gender, relation, account, share_percentage, nominee_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, gender, relation, account, share_percentage, nominee_type))

        conn.commit()

        return redirect("/view")

    except Exception as e:
        return f"ADD ERROR: {str(e)}"

    finally:
        cursor.close()
        conn.close()

# ---------------- View Jatin/Sunandana ----------------
@app.route("/view")
def view():
    try:
        search = request.args.get("search")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

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

    except Exception as e:
        return f"ERROR OCCURED: {str(e)}"

# ---------------- UPDATE  by Sunandana Sahoo----------------

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    try:
        name = request.form["name"]
        gender = request.form["gender"]
        relation = request.form["relation"]
        account = request.form["account"]
        nominee_type = request.form["nominee_type"]

        # ✅ FIX: remove %
        share_percentage = request.form["share_percentage"].replace("%", "")
        share_percentage = float(share_percentage)

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

        return redirect("/view")

    except Exception as e:
        return f"UPDATE ERROR: {str(e)}"

    finally:
        cursor.close()
        conn.close()

# ---------------- edit  by Sunandana Sahoo----------------
@app.route("/edit/<int:id>")
def edit(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM nominees WHERE id=%s", (id,))
    nominee = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit.html", nominee=nominee)

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