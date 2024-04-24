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
    curr.execute("select * from products order by id;")
    prods=curr.fetchall()
    # for prod in prods :   
    return prods


#write a function to get sales define a cfunction (def)

def calc_sales(): 
    curr.execute("select * FROM sales")
    sales=curr.fetchall()
    for sale in sales:
        return(sale)

# calc_sales()

def get_data(table_name):
    select=f"select * from {table_name} order by ID ASC;"
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
    pid, quantity = values[0], values[1]
    insert_sale="insert into sales(pid,quantity,created_at)values(%s,%s,now());"
    update_stock = "UPDATE products SET stock_quantity = stock_quantity - %s WHERE id = %s"

    try:
        # Insert sale record
        curr.execute(insert_sale, values)
        # Update stock quantity
        curr.execute(update_stock, (quantity, pid))
        conn.commit()
        print("Sale recorded successfully.")
    except Exception as e:
        conn.rollback()
        print("Error occurred while recording sale:", e)


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

# annual sale

def annual_sale():
    annual_sales="select extract(year from sales.created_at) AS year,sum(products.selling_price*sales.quantity) as Total_sales FROM products join sales on products.id=sales.pid Group by year Order by year;"
    curr.execute(annual_sales)
    data=curr.fetchall()
    return(data)


# profit per day

def daily_profit():
    profit="select date(sales.created_at) as day, sum(selling_price-buying_price) FROM products join sales on products.id=sales.pid Group by day Order by day;"
    curr.execute(profit)
    data=curr.fetchall()
    return(data)


# annual profit

def annual_profit():
    annual_profits="select extract(year from sales.created_at) AS year, sum(selling_price-buying_price) FROM products join sales on products.id=sales.pid Group by year Order by year;"
    curr.execute(annual_profits)
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
    curr.execute(insert,values)
    conn.commit()



# delete products

def delete_products(product_ids):
    if not product_ids:
        return "No product IDs provided for deletion."
    
    try:
        for product_id in product_ids:
            # Delete associated sales records for the product
            delete_sales_for_product(product_id)

        # Once associated sales records are deleted, delete the products
        placeholders = ', '.join(['%s'] * len(product_ids))
        delete_query = f"DELETE FROM products WHERE id IN ({placeholders});"
        curr.execute(delete_query, product_ids)
        conn.commit()

        return "Selected products deleted successfully."
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error deleting products: {e}"



def delete_sales_for_product(product_id):
    delete_query = "DELETE FROM sales WHERE pid = %s;"
    curr.execute(delete_query, (product_id,))
    conn.commit()


# delete_sale(9)

def delete_sale(id):
    # Delete the sale from the sales table
    delete_query = "DELETE FROM sales WHERE id = %s;"
    curr.execute(delete_query, (id,))
    conn.commit()


# search for a product
def search_result(product_name):
    search_query = "SELECT * FROM products WHERE name LIKE %s;"
    # Construct the wildcard search pattern
    search_pattern = '%' + str(product_name[0]) + '%'
    curr.execute(search_query, (search_pattern,))
    result = curr.fetchone()
    print("Search Query:", search_query)
    print("Search Pattern:", search_pattern)
    print("Result:", result)
    return result








   
    














