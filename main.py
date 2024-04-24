from flask import Flask,render_template,request, redirect, url_for, flash, session
from database import  get_products, annual_profit, annual_sale, search_result, insert_products, get_data, insert_sales, sales_product, profit_product, daily_sales, daily_profit, insert_users, check_email, check_logins, contact_us, delete_products


#create a flask instance

app = Flask(__name__)
app.secret_key = 'ksfgj'

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/home')
def home():
    if 'email_address' not in session:
        flash("You are not logged in", "error")
        return redirect(url_for("login"))
    
    username = session.get('username')
    if not username:
        # Handle the case when the username is not in the session
        flash("Username not found in session", "error")
        return redirect(url_for("login"))
    
    return render_template('home.html', username=username)


@app.route('/products')
def products():
    if 'email_address' not in session:
        flash("Login to Access This Page","error")
        return redirect(url_for('login'))
    
    prods=get_products( )
    return render_template("products.html",products=prods,id=id)

@app.route('/sales')
def sales ():
    if 'email_address' not in session:
        flash("Login to Access This Page","error")
        return redirect(url_for('login'))

    prods = get_products( )
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
    try:
        pid = request.form['pid']
        quantity = int(request.form['quantity'])
        
        # Perform input validation
        if not pid or quantity <= 0:
            flash("Invalid input. Please provide a valid product ID and quantity.", "error")
            return redirect(url_for('sales'))
        
        sale = (pid, quantity)
        insert_sales(sale)
        flash("Sale recorded successfully.", "success")
    except Exception as e:
        # Handle errors
        flash(f"Error occurred while recording sale: {str(e)}", "error")
    return redirect(url_for('sales'))


@app.route('/dashboard')
def dashboard():
    if 'email_address' not in session:
        flash("You are not logged in","error")
        return redirect(url_for("login"))
    # If user is not logged in, redirect to login page

    an=annual_sale()
    year=[]
    total=[]
    for i in an:
        year.append(str(i[0]))
        total.append(f"{float(i[1]):.2f}")

    sp = sales_product()
    names = []
    value = []
    for i in sp:
        names.append(str(i[0]))
        value.append(float(i[1]))

    pp = profit_product()
    name = []
    profit = []
    for i in pp:
        name.append(str(i[0]))
        profit.append(float(i[1]))

    # Sales per day on a line chart
    ds = daily_sales()
    day = []
    sl = []
    for i in ds:
        day.append(str(i[0]))
        sl.append(float(i[1]))

    dp = daily_profit()
    daily = []
    profits = []
    for i in dp:
        daily.append(str(i[0]))
        profits.append(float(i[1]))

    ap=annual_profit()
    yearly= []
    annualprofits = []
    for i in ap:
        yearly.append(str(i[0]))
        annualprofits.append(f"{float(i[1]):.2f}")

    return render_template('dashboard.html', yearly=yearly, annualprofits=annualprofits, year=year, total=total, len=len,  names=names, value=value, name=name, profit=profit, day=day, sl=sl, daily=daily, profits=profits)

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
            session['email_address'] = email_address  # Store email address in session
            session['full_name'] = full_name 
        return redirect(url_for('login'))
    return render_template("registration.html")



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        email_address = request.form['email_address']
        password = request.form['password']

        username = email_address.split('@')[0]
        
        if check_logins(email_address, password):
            # If login is successful, set session data and redirect to dashboard
            session['email_address'] = email_address
            session['username'] = username
            flash("Access granted", "success")
            return redirect(url_for("home"))
        else:
            flash("Wrong email address or password. Please try again.","error")
      
    return render_template("login.html")


@app.route('/logout')
def logout():
   
    session.pop('email_address', None)
    flash("Logged Out", "success")
    return redirect(url_for('home'))


@app.route('/contact')
def contact():
    return render_template("contact.html")


# delete multiple products at once

@app.route('/delete_products', methods=['POST'])
def delete_prods():
    if request.method == 'POST':
        product_ids = request.form.getlist('product_ids[]')
        result_message = delete_products(product_ids)
        flash(result_message, "success")
        return redirect(url_for('products')) 


@app.route('/search', methods=['GET'])

def search_results():
    search_query = request.args.get('query')
   
    if search_query:
        products = get_products()  # Fetch all products from the database
        filtered_products = [product for product in products if search_query.lower() in product[1].lower()]  # Filter products based on the search query
    else:
        filtered_products = []

    return render_template('products.html', search_query=search_query, products=filtered_products)


app.run(debug=True)