from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE = "data.json"

# create file if not exists
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

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append({
        "name": name,
        "gender": gender,
        "relation": relation,
        "account": account,
        "share_percentage": share_percentage,
        "nominee_type": nominee_type
    })

    with open(FILE, "w") as f:
        json.dump(data, f)

    return redirect("/view")


# ---------------- VIEW ----------------
@app.route("/view")
def view():
    with open(FILE, "r") as f:
        data = json.load(f)

    return render_template("view.html", nominees=data)


# ---------------- EDIT ----------------
@app.route("/edit/<int:index>")
def edit(index):
    with open(FILE, "r") as f:
        data = json.load(f)

    nominee = data[index]

    return render_template("edit.html", nominee=nominee, index=index)


# ---------------- UPDATE ----------------
@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    with open(FILE, "r") as f:
        data = json.load(f)

    data[index]["name"] = request.form["name"]
    data[index]["gender"] = request.form["gender"]
    data[index]["relation"] = request.form["relation"]
    data[index]["account"] = request.form["account"]
    data[index]["share_percentage"] = request.form["share_percentage"]
    data[index]["nominee_type"] = request.form["nominee_type"]

    with open(FILE, "w") as f:
        json.dump(data, f)

    return redirect("/view")


# ---------------- DELETE ----------------
@app.route("/delete/<int:index>")
def delete(index):
    with open(FILE, "r") as f:
        data = json.load(f)

    if index < len(data):
        data.pop(index)

    with open(FILE, "w") as f:
        json.dump(data, f)

    return redirect("/view")


# ---------------- API endpoint ----------------
@app.route("/api/nominees")
def api_nominees():
    with open(FILE, "r") as f:
        data = json.load(f)

    return {"nominees": data}

# ---------------- Total nominees ----------------

@app.route("/dashboard")
def dashboard():
    with open(FILE, "r") as f:
        data = json.load(f)

    total = len(data)

    return render_template("dashboard.html", total=total)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5007)