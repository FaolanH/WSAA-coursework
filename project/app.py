app = Flask(__name__)

DB = "hpm08.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/hpm08")
def hpm08_list():
    conn = get_db()
    rows = conn.execute("SELECT * FROM hpm08 ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("hpm08_list.html", rows=rows)

@app.route("/hpm08/add", methods=["GET", "POST"])
def hpm08_add():
    if request.method == "POST":
        period = request.form["period"]
        geography = request.form["geography"]
        value = request.form["value"]

        conn = get_db()
        conn.execute(
            "INSERT INTO hpm08 (period, geography, value) VALUES (?, ?, ?)",
            (period, geography, value)
        )
        conn.commit()
        conn.close()

        return redirect("/hpm08")

    return render_template("hpm08_add.html")

@app.route("/hpm08/edit/<int:id>", methods=["GET", "POST"])
def hpm08_edit(id):
    conn = get_db()

    if request.method == "POST":
        period = request.form["period"]
        geography = request.form["geography"]
        value = request.form["value"]

        conn.execute(
            "UPDATE hpm08 SET period=?, geography=?, value=? WHERE id=?",
            (period, geography, value, id)
        )
        conn.commit()
        conn.close()
        return redirect("/hpm08")

    row = conn.execute("SELECT * FROM hpm08 WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("hpm08_edit.html", row=row)

@app.route("/hpm08/delete/<int:id>")
def hpm08_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM hpm08 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/hpm08")



