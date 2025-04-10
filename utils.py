import sqlite3

def check_budget(conn, category_id, month):
    cursor = conn.cursor()
    cursor.execute("select sum(amount) from expenses where category_id = ? and strftime('%Y-%m', date) = ?", (category_id, month))
    total_spent = cursor.fetchone()[0] or 0

    cursor.execute("select amount from budgets where category_id = ? and month = ?", (category_id, month))
    row = cursor.fetchone()
    if row:
        budget_amt = row[0]
        if total_spent > budget_amt:
            print("Alert: Budget Exceeded!")
        elif total_spent > 0.9 * budget_amt:
            print("Alert: You’ve used 90% of your budget!")

def monthly_report(month):
    conn = sqlite3.connect("database/expense_tracker.db")
    cursor = conn.cursor()

    cursor.execute("select c.name, sum(e.amount) from expenses e join categories c on e.category_id = c.id where strftime('%Y-%m', e.date) = ? group by c.name", (month,))
    expenses = cursor.fetchall()

    report = []
    for cat, total in expenses:
        cursor.execute("select amount from budgets b join categories c on b.category_id = c.id where c.name = ? and b.month = ?", (cat, month))
        row = cursor.fetchone()
        budget_amt = row[0] if row else 0
        report.append((cat, total, budget_amt))

    return report