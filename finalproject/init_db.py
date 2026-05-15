import sqlite3
import json
connection = sqlite3.connect("dosa.db")
cursor = connection.cursor()

#Costomers
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);
""")

#Items
cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,         
    price REAL NOT NULL
);
""")

#order
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cust_id INT NOT NULL,
    notes TEXT,
    FOREIGN KEY(cust_id) REFERENCES customer(id)
);
""")

#Junction table(order_Items)
cursor.execute("""
CREATE TABLE IF NOT EXISTS item_list(
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    PRIMARY KEY(order_id, item_id),
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")
customers = {}
items = {}

with open("example_orders.json") as data:
    orders = json.load(data)
    for order in orders:
        if order["phone"] not in customers:
            customers[order["phone"]] = order["name"]
        for item in order["items"]:
            name = item["name"]
            price = item["price"]
            if name not in items:
                items[name] = price
for phone in customers:
    name = customers[phone]
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name,
phone))
    
for name in items:
    price = items[name]
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))
for order in orders:
    ts = order["timestamp"]
    notes = order["notes"]
    phone = order["phone"]
    cust_id = cursor.execute("SELECT id FROM customers WHERE phone=?",
(phone,)).fetchone()[0]
    cursor.execute(
        "INSERT INTO orders (timestamp, cust_id, notes) VALUES (?, ?, ?);",
        (ts, cust_id, notes))
    order_id = cursor.lastrowid
    for item in order["items"]:
        name = item["name"]
        item_id = cursor.execute("SELECT id FROM items WHERE name=?",
(name,)).fetchone()[0]
    cursor.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);",
(order_id, item_id))

connection.commit()

connection.close()

print("YOU THE FREAKING WORKED")