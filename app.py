from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
from utils import check_budget, monthly_report

app = Flask(__name__)
DB_PATH = "database/expense_tracker.db"

@app.route("/")
def index():
    return render_template("index.html")

# set monthly budget functionality
@app.route("/setBudget", methods=["GET", "POST"])
def set_budget():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == "POST":
        category = request.form["category"]
        month = request.form["month"]
        amount = float(request.form["amount"])

        cursor.execute("select id from categories where name=?", (category,))
        row = cursor.fetchone()
        
        if row:
            cat_id = row[0]
        else:
            cursor.execute("insert into categories (name) values (?)", (category,))
            conn.commit()
            cat_id = cursor.lastrowid

        cursor.execute("insert into budgets (category_id, month, amount) values (?, ?, ?)", (cat_id, month, amount))
        conn.commit()
        return redirect(url_for("index"))

    return render_template("set_budget.html")

# add expenses
@app.route("/addExpense", methods=["GET", "POST"])
def add_expense():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        date = request.form["date"] or str(datetime.date.today())

        cursor.execute("select id from categories where name=?", (category,))
        row = cursor.fetchone()
        if row:
            cat_id = row[0]
        else:
            cursor.execute("insert into categories (name) values (?)", (category,))
            conn.commit()
            cat_id = cursor.lastrowid

        cursor.execute("insert into expenses (amount, date, category_id) values (?, ?, ?)", (amount, date, cat_id))
        conn.commit()
        check_budget(conn, cat_id, date[:7])
        return redirect(url_for("index"))

    return render_template("add_expense.html")

# view all reports
@app.route("/viewReport", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        month = request.form["month"]
        data = monthly_report(month)
        return render_template("my_reports.html", month=month, data=data)
    return render_template("my_reports.html", data=None)

if __name__ == "__main__":
    app.run()