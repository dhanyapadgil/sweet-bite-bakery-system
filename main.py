from tabulate import tabulate
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",
        database="bakery_db")
def add_product():
    db = connect_db()
    cursor = db.cursor()

    name = input("Enter product name: ")
    category = input("Enter category: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))
    expiry = input("Enter expiry date (YYYY-MM-DD): ")

    query = """
    INSERT INTO products (name, category, price, stock, expiry_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, category, price, stock, expiry))
    db.commit()

    print(" Product added successfully!")

    db.close()

def view_products():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM products ORDER BY category, product_id")

    products = cursor.fetchall()

    headers = ["Product ID", "Name", "Category", "Price", "Stock", "Expiry Date"]

    if products:
        print("\n--- PRODUCT LIST ---")
        print(tabulate(products, headers=headers, tablefmt="grid"))
    else:
        print("No products found.")

    db.close()

def product_menu():
    while True:
        print("\n--- PRODUCT MANAGEMENT ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            break
        else:
            print(" Invalid choice, try again!")


def view_products():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT product_id, name, category, price, stock, expiry_date
        FROM products
        ORDER BY product_id
    """)

    products = cursor.fetchall()

    headers = ["Product ID", "Name", "Category", "Price", "Stock", "Expiry Date"]

    print("\n--- BAKERY MENU ---")
    print(tabulate(products, headers=headers, tablefmt="grid"))

    db.close()


def add_ingredient():
    db = connect_db()
    cursor = db.cursor()

    name = input("Enter ingredient name: ")
    quantity = float(input("Enter quantity: "))
    unit = input("Enter unit (kg/grams/litres/pieces): ")
    date = input("Enter last updated date (YYYY-MM-DD): ")

    query = """
    INSERT INTO inventory (name, quantity, unit, last_updated)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, quantity, unit, date))
    db.commit()

    print("Ingredient added successfully!")

    db.close()

def view_inventory():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    headers = ["ID", "Ingredient", "Quantity", "Unit", "Last Updated"]

    if items:
        print("\n--- INVENTORY LIST ---")
        print(tabulate(items, headers=headers, tablefmt="grid"))
    else:
        print("Inventory is empty.")

    db.close()
def inventory_menu():
    while True:
        print("\n--- INVENTORY MANAGEMENT ---")
        print("1. Add Ingredient")
        print("2. View Inventory")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_ingredient()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            break
        else:
            print(" Invalid choice")


def place_order():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT product_id, name, price, stock FROM products WHERE stock > 0")
    products = cursor.fetchall()

    if not products:
        print("No products available.")
        return

    print("\n--- AVAILABLE PRODUCTS ---")
    print(tabulate(products, headers=["ID", "Name", "Price", "Stock"], tablefmt="grid"))

    product_id = int(input("Enter Product ID to order: "))
    quantity = int(input("Enter quantity: "))

    cursor.execute(
        "SELECT price,cost_price, stock FROM products WHERE product_id = %s",
        (product_id,))
    product = cursor.fetchone()

    if not product:
        print("Invalid product.")
        return

    price,cost_price, stock = product

    if quantity > stock:
        print("Not enough stock available.")
        return

    total = price * quantity
    profit = (price - cost_price) * quantity
    
    cursor.execute(
        "INSERT INTO orders (order_date, total_amount) VALUES (CURDATE(), %s)",
        (total,))
    order_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
        (order_id, product_id, quantity, price))

    cursor.execute(
        "UPDATE products SET stock = stock - %s WHERE product_id = %s",
        (quantity, product_id))

    db.commit()

    # SHOW UPDATED TABLE
    cursor.execute("SELECT product_id, name, price, stock FROM products")
    updated_products = cursor.fetchall()

    print("\n--- UPDATED PRODUCT STOCK ---")
    print(tabulate(updated_products, headers=["ID", "Name", "Price", "Stock"], tablefmt="grid"))

    db.close()

    print("\n Order placed successfully! Total bill: ₹",total)



def view_orders():
    db = connect_db()
    cursor = db.cursor()

    query = """
    SELECT 
        o.order_id,
        o.order_date,
        p.name,
        oi.quantity,
        oi.price,
        o.total_amount
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    ORDER BY o.order_id
    """

    cursor.execute(query)
    orders = cursor.fetchall()

    headers = ["Order ID", "Date", "Product", "Quantity", "Price", "Total Bill"]

    if not orders:
        print("No orders placed yet.")
    else:
        print("\n--- ORDER HISTORY ---")
        print(tabulate(orders, headers=headers, tablefmt="grid"))

    db.close()

from tabulate import tabulate
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="trust",
        database="bakery_db"
    )

def daily_sales_report(date, orders):
    """
    orders: list of tuples -> (sale_amount, cost_amount)
    """
    total_orders = len(orders)
    total_sales = sum(sale for sale, cost in orders)
    total_profit = sum(sale - cost for sale, cost in orders)

    # Save to SQL
    save_daily_report(date, total_sales, total_orders, total_profit)

    # Display as table
    table = [["Total Orders", total_orders],
             ["Total Sales", f"₹{total_sales}"],
             ["Total Profit", f"₹{total_profit}"]]
    print(tabulate(table, headers=["Metric", "Value"], tablefmt="grid"))

    db.close()

def low_stock_alert():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT product_id, name, stock
        FROM products
        WHERE stock < 5
    """)
    low_stock_items = cursor.fetchall()

    if not low_stock_items:
        print("\n All products are sufficiently stocked.")
    else:
        print("\n⚠️ LOW STOCK ALERT ⚠️")
        print(tabulate(
            low_stock_items,
            headers=["Product ID", "Product Name", "Stock Left"],
            tablefmt="grid"))

    db.close()

def view_invoice():
    db = connect_db()
    cursor = db.cursor()

    order_id = int(input("Enter Order ID to view bill: "))

    cursor.execute("""
        SELECT 
            o.order_id,
            o.order_date,
            p.name,
            oi.quantity,
            oi.price,
            (oi.quantity * oi.price) AS item_total
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.order_id = %s
    """, (order_id,))

    items = cursor.fetchall()

    if not items:
        print("Order not found.")
        return

    headers = ["Order ID", "Date", "Product", "Qty", "Price", "Item Total"]

    print("\n BAKERY INVOICE")
    print(tabulate(items, headers=headers, tablefmt="grid"))

    # calculate grand total
    grand_total = sum(item[5] for item in items)

    print("\n GRAND TOTAL: ₹",{grand_total})

    db.close()

def restock_product():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT product_id, name, stock FROM products")
    products = cursor.fetchall()

    if not products:
        print("No products found.")
        return

    print("\n--- CURRENT PRODUCT STOCK ---")
    print(tabulate(products, headers=["ID", "Name", "Stock"], tablefmt="grid"))

    product_id = int(input("Enter Product ID to restock: "))
    add_qty = int(input("Enter quantity to add: "))

    if add_qty <= 0:
        print("Quantity must be greater than zero.")
        return

    cursor.execute(
        "UPDATE products SET stock = stock + %s WHERE product_id = %s",
        (add_qty, product_id))

    db.commit()

    cursor.execute("SELECT product_id, name, stock FROM products WHERE product_id = %s", (product_id,))
    updated = cursor.fetchone()

    print("\n PRODUCT RESTOCKED SUCCESSFULLY")
    print(tabulate([updated], headers=["ID", "Name", "Updated Stock"], tablefmt="grid"))

    db.close()

def top_selling_product():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            p.product_id,
            p.name,
            SUM(oi.quantity) AS total_quantity_sold,
            SUM(oi.quantity * oi.price) AS total_revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_quantity_sold DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    if not result:
        print("No sales data available yet.")
    else:
        print("🏆 TOP SELLING PRODUCT ")
        print(tabulate(
            [result],
            headers=["Product ID", "Product Name", "Quantity Sold", "Revenue"],
            tablefmt="grid"))

    db.close()

def monthly_sales_report():
    db = connect_db()
    cursor = db.cursor()

    # monthly summary
    cursor.execute("""
        SELECT 
            DATE_FORMAT(order_date, '%Y-%m') AS month,
            COUNT(order_id) AS total_orders,
            IFNULL(SUM(total_amount), 0) AS total_sales
        FROM orders
        GROUP BY month
        ORDER BY month
    """)

    months = cursor.fetchall()

    if not months:
        print("No sales data available yet.")
    else:
        print("📊 MONTHLY SALES REPORT")
        print(tabulate(
            months,
            headers=["Month", "Total Orders", "Total Sales (₹)"],
            tablefmt="grid"))

    db.close()

def daily_sales_report():
    db = connect_db()
    cursor = db.cursor()

    # Fetch today's totals
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT o.order_id),
            IFNULL(SUM(o.total_amount), 0),
            IFNULL(SUM((oi.price - p.cost_price) * oi.quantity), 0)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.order_date = CURDATE()
    """)

    total_orders, total_sales, total_profit = cursor.fetchone()

    # Convert to integers for clean display
    total_orders = int(total_orders)
    total_sales = int(total_sales)
    total_profit = int(total_profit)

    # Make a table
    table = [
        ["Total Orders Today", total_orders],
        ["Total Sales Today", f"₹{total_sales}"],
        ["Total Profit Today", f"₹{total_profit}"]
    ]

    print("\n=== DAILY SALES REPORT ===")
    print(tabulate(table, headers=["Metric", "Value"], tablefmt="grid"))

    db.close()

def view_invoice():
    db = connect_db()
    cursor = db.cursor()

    order_id = int(input("Enter Order ID to view bill: "))

    cursor.execute("""
        SELECT 
            o.order_id,
            o.order_date,
            p.name,
            oi.quantity,
            oi.price,
            p.cost_price,
            (oi.quantity * oi.price) AS item_total,
            (oi.quantity * (oi.price - p.cost_price)) AS item_profit
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.order_id = %s
    """, (order_id,))

    items = cursor.fetchall()

    if not items:
        print("Order not found.")
        return

    headers = ["Order ID", "Date", "Product", "Qty", "Price", "Cost Price", "Item Total", "Profit"]

    print("\n🧾 BAKERY INVOICE WITH PROFIT")
    print(tabulate(items, headers=headers, tablefmt="grid"))

    # calculate grand total & total profit
    grand_total = sum(item[6] for item in items)
    total_profit = sum(item[7] for item in items)

    print("💰GRAND TOTAL: ₹",{grand_total})
    print("💸TOTAL PROFIT: ₹",{total_profit})

    db.close()

def delete_order():
    db = connect_db()
    cursor = db.cursor()

    order_id = int(input("Enter Order ID to delete: "))

    # Check if order exists
    cursor.execute(
        "SELECT product_id, quantity FROM order_items WHERE order_id = %s",
        (order_id,))
    items = cursor.fetchall()

    if not items:
        print("Order not found.")
        db.close()
        return

    # Restore stock
    for product_id, quantity in items:
        cursor.execute(
            "UPDATE products SET stock = stock + %s WHERE product_id = %s",
            (quantity, product_id))

    # Delete order items
    cursor.execute(
        "DELETE FROM order_items WHERE order_id = %s",
        (order_id,))

    # Delete order
    cursor.execute(
        "DELETE FROM orders WHERE order_id = %s",
        (order_id,))

    db.commit()
    db.close()

    print("Order deleted successfully and stock restored.")


def main_menu():
    while True:
        print("\n=== BAKERY MANAGEMENT SYSTEM ===")
        print("1. Product Management")
        print("2. Inventory Management")
        print("3. Place Order")
        print("4. View Order")
        print("5. Delete Order")
        print("6. Daily Sales Report")
        print("7. Low Stock Alert")
        print("8. View Invoice")
        print("9. Restock Product")
        print("10. Top Selling Product")
        print("11. Monthly Sales Report")
        print("12. View Invoice")
        print("13. Exit") 

        choice = input("Enter your choice: ")

        if choice == "1":
            product_menu()
        elif choice == "2":
            inventory_menu()
        elif choice == "3":
            place_order()
        elif choice == "4":
            view_orders()
        elif choice == "5":
            delete_order()
        elif choice == "6":
            daily_sales_report()
        elif choice == "7":
            low_stock_alert()
        elif choice == "8":
            view_invoice()
        elif choice == "9":
            restock_product()
        elif choice == "10":
            top_selling_product()
        elif choice == "11":
            monthly_sales_report()
        elif choice == "12":
            view_invoice()
        elif choice == "13":
            print("Thank you 😁 ")
            break


main_menu()
