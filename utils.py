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