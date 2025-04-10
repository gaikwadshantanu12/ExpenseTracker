import sqlite3

db_path = "database/expense_tracker.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Categories table
categories_sql = 'create table if not exists categories(id integer primary key autoincrement, name text unique not null)'
cursor.execute(categories_sql)

# Create Expenses table
expenses_sql = 'create table if not exists expenses(id integer primary key autoincrement, amount real not null, date text not null, category_id integer, foreign key(category_id) references categories(id))'
cursor.execute(expenses_sql)

# Create Budgets table
budgets_sql = 'create table if not exists budgets(id integer primary key autoincrement, category_id integer, month text, amount real not null, foreign key(category_id) references categories(id))'
cursor.execute(budgets_sql)

conn.commit()
conn.close()

print("Database Table Created !!")
