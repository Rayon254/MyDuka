import psycopg2

#connect to database 

conn=psycopg2.connect(
    user="postgres",
    dbname="myduka",
    password="1234",
    port=5432,
    host='localhost'
)

curr=conn.cursor()  # used to perform data operations i.e select, update

def get_products():
    curr.execute("select * from products;")
    prods=curr.fetchall()
    for prod in prods :   
        print(prod)

get_products()


#write a function to get sales define a cfunction (def)

def calc_sales():
    curr.execute("select * FROM sales")
    sales=curr.fetchall()
    for sale in sales:
        print(sale)

# calc_sales()

def get_data(table_name):
    select=f"select * from {table_name};"
    curr.execute(select)  # contains the sql querry you want to run   curr=cursor.execute
    data=curr.fetchall()
    return(data)
        


# insert data

def insert_products(values):
    insert="insert into products(name,buying_price,\
        selling_price,stock_quantity)values(%s,%s,%s,%s);"
    curr.execute(insert,values)
    conn.commit()

# items=("tilapia",200,500,8)
# insert_product(items)


# insert sales
def insert_sales(values):
    insert="insert into sales(pid,quantity,created_at)values(%s,%s,now());"

    curr.execute(insert,values)
    conn.commit()

#sales per product
def sales_product():
    display="select name,sum(selling_price*quantity) FROM products join sales on products.id=sales.pid Group by name;"
    curr.execute(display)
    data=curr.fetchall()
    return(data)

# profit per product

def profit_product():
    profit="select name,sum(selling_price-buying_price) FROM products Group by name;"
    curr.execute(profit)
    data=curr.fetchall()
    return(data)

# sales per day

def daily_sales():
    dailysales="select date(sales.created_at) as day,sum(selling_price*quantity) FROM products join sales on products.id=sales.pid Group by day Order by day;"
    curr.execute(dailysales)
    data=curr.fetchall()
    return(data)

# profit per day

def daily_profit():
    profit="select date(sales.created_at) as day, sum(selling_price-buying_price) FROM products join sales on products.id=sales.pid Group by day Order by day;"
    curr.execute(profit)
    data=curr.fetchall()
    return(data)


#insert users 

def insert_users(values):
    insert="insert into users(full_name,email_address,password)values(%s,%s,%s);"
    curr.execute(insert,values)
    conn.commit()

# user=("Ann","ann@gmail.com",5008)
# insert_users(user)

# =>write a query that checks if the provide email is already in the database(exists)

def check_email(email):
    query="select exists (select email_address from users where email_address = %s);"
    curr.execute(query,(email,))
    exist=curr.fetchone()[0]
    return(exist)

#check if logins exist/match

def check_logins(email_address,password):
    query="select * from users where email_address=%s and password=%s;"
    curr.execute(query,(email_address,password,))
    check=curr.fetchone()
    return(check)

def contact_us(values):
    insert="insert into contacts(full_name,email_address,phone_number,message)values(%s,%s,%s,%s);"
    curr.execute(insert,values)
    conn.commit()



# delete a product

def delete_product(id):
    try:
        # Delete associated records in the sales table first
        delete_sales_query = "DELETE FROM sales WHERE pid = %s;"
        curr.execute(delete_sales_query, (id,))
        conn.commit()
        
        # Then delete the product from the products table
        delete_product_query = "DELETE FROM products WHERE id = %s;"
        curr.execute(delete_product_query, (id,))
        conn.commit()

        return("Product deleted successfully.")
    except psycopg2.Error as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        return(f"Error deleting product: {e}")


# edit a product

def edit_product(id, new_product_name, new_buying_price, new_selling_price, new_stock_quantity):
    update_query = "UPDATE products SET product_name = %s, buying_price = %s, selling_price = %s, stock_quantity = %s WHERE id = %s;"
    curr.execute(update_query, (new_product_name, new_buying_price, new_selling_price, new_stock_quantity, id))
    conn.commit()







