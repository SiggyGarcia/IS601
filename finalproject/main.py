from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def connect_to_db():
    connection = sqlite3.connect("dosa.db")
    cursor = connection.cursor()
    return connection, cursor

class Customer(BaseModel):
    name:str
    phone: str


@app.get("/customers/{id}")
async def get_customer(id: int):
   conn, cursor = connect_to_db()
   row = cursor.execute(
       "SELECT id,name, phone FROM customers WHERE id=?",
       (id,)
    ).fetchone() 
   conn.close()

   if row == None:
       raise HTTPException(status_code=404, detail="Customers not found" )
   return {"id": row[0], "name": row[1], "phone": row[2]}


   if id in customers:
       return customers[id]
   raise HTTPException(status_code=404, detail="Customers not found")

@app.get("/customers")
async def get_all_customers():
    conn, cursor = connect_to_db()

    cursor.execute("SElECT id, name, phone FROM customers")
    rows = cursor.fetchall()
    conn.close()

    customer_list = [
        {"id": row[0], "name":row[1], "phone": row[2]}
        for row in rows
    ]
    return customer_list

@app.put("/custmers/{id}")

async def update_customer(id: int, customer: Customer):
    conn, cursor = connect_to_db()

    cursor.execute(
        "UPDATE customers SET name = ?, phone = ? WHERE id = ?",
        (customer.name, customer.phone, id)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return{"id":id, "name": customer.name, "phone": customer.phone}


@app.delete("/customers/{id}")
async def delete_cutomers(id: int):
    conn, cursor = connect_to_db()
    
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    deleted = cursor.rowcount > 0

    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"message": f"Customers{id} deleted successfully"}

@app.post("/customers")
async def create_customer(customer:Customer):
     conn, cursor = connect_to_db()

     cursor.execute(
         "INSERT INTO customers(name, phone) VALUES(?, ?)",
         (customer.name, customer.phone)
     )
     conn.commit()

     new_id = cursor.lastrowid
     conn.close()
     return {"id": new_id, "name": customer.name, "phone": customer.phone }
 




@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"id":id}