# Sweet Bite Bakery System

A terminal-based bakery management system built with **Python** and **MySQL** as a Class 12 school project.

Handles everything a small bakery needs — products, inventory, orders, billing, and sales reports — all from the command line.

---

## Features

- Add and view bakery products with expiry dates
- Manage ingredient inventory (add, view)
- Place orders and auto-update stock
- View full order history
- Delete orders and restore stock automatically
- Generate daily and monthly sales reports
- Low stock alerts (warns when stock drops below 5)
- View itemised invoice with profit breakdown
- Restock products
- See the top-selling product by quantity

---

## Tech stack

| Technology | Purpose |
|------------|---------|
| Python 3   | Application logic and CLI menus |
| MySQL      | Database — products, orders, inventory |
| mysql-connector-python | Python-MySQL connection |
| tabulate   | Clean table display in terminal |

---

## Project structure

```
sweet-bite-bakery-system/
├── main.py          # Full application — all menus and features
├── bakery_db.sql    # Database schema + sample data
└── README.md        # This file
```

---

## How to run

### 1. Install required Python libraries
```
pip install mysql-connector-python tabulate
```

### 2. Set up the database
Open MySQL and run:
```
source bakery_db.sql
```
This creates the `bakery_db` database with all tables and sample data.

### 3. Update your MySQL password in main.py
Open `main.py` and find the `connect_db()` function:
```python
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",  # change this
        database="bakery_db"
    )
```
Replace `your_password_here` with your own MySQL root password.

### 4. Run the app
```
python main.py
```

---

## Database tables

| Table | Description |
|-------|-------------|
| `products` | Bakery items with price, cost price, stock, expiry |
| `inventory` | Raw ingredients with quantity and unit |
| `orders` | Order records with date and total amount |
| `order_items` | Individual items linked to each order |

---

## Sample data included

The `.sql` file includes 4 sample products (Chocolate Cake, Croissant, Muffin, Bread) and 5 ingredients so you can test the system right away.

---

## About

Built by **Dhanya Padgil** as a Class 12 school project in Indore, MP.
My first project combining Python with a real relational database.
Learned SQL JOINs, Python functions, and how to build a full menu-driven CLI app.

---

## License

Open source — feel free to use, modify, or improve this project.
