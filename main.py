from flask import Flask,render_template,request, redirect, url_for, flash, session
from database import insert_products, get_data, insert_sales, sales_product, profit_product, daily_sales, daily_profit, insert_users, check_email, check_logins, contact_us, delete_product, edit_product


#create a flask instance

app = Flask(__name__)
app.secret_key = 'ksfgj'

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/products')
def products():
    if 'email_address' not in session:
        flash("Login to Access This Page","error")
    return redirect(url_for('login'))

    prods=get_data("products")
    return render_template("products.html",products=prods)

@app.route('/sales')
def sales ():
    # if 'email_address' not in session:
    #     flash("Login to Access This Page")
    #     return redirect(url_for('sales'))

    prods = get_data("products")
    sale=get_data("sales")
    return render_template('sales.html',sales=sale,products=prods)


@app.route('/add_products', methods=['POST'])
def add_products():

    product_name = request.form['product_name']
    buying_price = request.form['buying_price']
    selling_price = request.form['selling_price']
    stock_quantity = request.form['stock_quantity']
    
    value=product_name, buying_price, selling_price, stock_quantity
    
    insert_products(value)

    return redirect(url_for('products'))        


@app.route('/make_sales', methods=['POST'])
def make_sales():
    
    pid=request.form['pid']
    quantity=request.form['quantity']
    sale=(pid,quantity)
    insert_sales(sale)
    return redirect(url_for('sales'))


@app.route('/dashboard')
def dashboard():
    if 'email_address' not in session:
        # Render dashboard template
        return redirect(url_for("login"))
    else:
        # If user is not logged in, redirect to login page
          
        sp=sales_product()
        names=[]
        value=[]
        for i in sp:
            names.append(str(i[0]))
            value.append(float(i[1]))

        pp=profit_product()
        names=[]
        profit=[]
        for i in pp:
            names.append(str(i[0]))
            profit.append(float(i[1]))

        
    #sales per day on a line chart 

    ds=daily_sales()
    day=[]
    sl=[]

    for i in ds:
        day.append(str(i[0]))
        sl.append(float(i[1]))

    dp=daily_profit()
    day=[]
    profit=[]

    for i in dp:
        day.append(str(i[0]))
        profit.append(float(i[1]))

    return render_template('dashboard.html',names=names,value=value, profit=profit, day=day,sl=sl)


 # insert users from registration

@app.route('/registration', methods=['POST', 'GET'])
def registration():

    if request.method=='POST':

        full_name = request.form['full_name']
        email_address = request.form['email_address']
        password = request.form['password']
        value=(full_name,email_address,password)
     
        if check_email(email_address):
            flash("Email already exists","error")
            return redirect(url_for('registration'))
        else:
            insert_users(value)
            flash("Registration Successful", "success")
        return redirect(url_for('login'))
    return render_template("registration.html")



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        
        if check_logins(email_address, password):
            # If login is successful, set session data and redirect to dashboard
            session['email_address'] = email_address
            flash("Access granted", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong email address or password. Please try again.","error")
      
    return render_template("login.html")


@app.route('/logout')
def logout():
   
    session.pop('email_address', None)
    return redirect(url_for('login'))


@app.route('/contact', methods=['POST','GET'])
def contact():

    full_name = request.form['full_name']
    email_address = request.form['email_address']
    phone_number = request.form['phone_number']
    message = request.form['message']
    value=(full_name,email_address,phone_number,message)
    contact_us(value)
    flash("Message Sent")
    return render_template("contact.html")

# delete a product a
@app.route('/delete_product/<int:id>', methods=['POST','DELETE'])
def delete_prod(id):
   
    delete_product(id)
    flash("Product deleted successfully.", "success")
    return redirect(url_for('products'))

# delete multiple products at once


@app.route('/delete_products', methods=['POST'])
def delete_all():

    product_ids = request.form.getlist('product_ids[]')  # Assuming the product IDs are sent as an array from the frontend
    for id in product_ids:
        delete_product(id)
    flash("Products deleted successfully", "success")
    return redirect(url_for('products'))


@app.route('/edit_product/', methods=['POST','GET'])
def edit_prod():
    if request.method == 'POST':
        id = request.form['id']
        new_product_name = request.form['new_product_name']
        new_buying_price = request.form['new_buying_price']
        new_selling_price = request.form['new_selling_price']
        new_stock_quantity = request.form['new_stock_quantity']
        
        # Call the function to edit the product in the database
        edit_product(id, new_product_name, new_buying_price, new_selling_price, new_stock_quantity)
        
        # Redirect back to the products page or wherever you want
        return redirect(url_for('products'))
    else:
        # Handle other HTTP methods if necessary
        return redirect(url_for('products'))


@app.route('/search_results', methods=['GET'])
def search_results():
    products=get_data("products")
    return render_template('products.html')


app.run(debug=True)