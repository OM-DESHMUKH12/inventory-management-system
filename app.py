from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_session import Session
# from get_sql_connection import get_sql_connection
import mysql.connector

def get_sql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MYSQL@123",
        database="inventory_db"
    )

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn =  get_sql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items = items)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        conn = get_sql_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",(username, email, hashed_password))
            conn.commit()
        except mysql.connector.IntegrityError:
            flash("Username or Email already exists!", "danger")
        
        cursor.close()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_sql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            session['user_id'] = user_data['user_id']
            session['username'] = user_data['username']
            return redirect(url_for('index'))  
        
        flash('Invalid email or password', 'danger') 

    return render_template('login.html')  



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':  # Handle form submission
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not name or not quantity or not price:
            flash("All fields are required!", "danger")
            return redirect(url_for('add_item'))

        conn = get_sql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO inventory (name, quantity, price) VALUES (%s, %s, %s)', (name, quantity, price))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Item added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_item.html')  # Show the form when accessed via GET

    

@app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_sql_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        item_id = request.form.get('item_id')  # Get item_id from form
        item_name = request.form.get('name')
        item_quantity = request.form.get('quantity')
        item_price = request.form.get('price')

        if not item_id:  # Ensure an item is selected
            flash('Please select an item to update.', 'danger')
            return redirect(url_for('update_item'))

        cursor.execute('UPDATE inventory SET name = %s, quantity = %s, price = %s WHERE item_id = %s', 
                       (item_name, item_quantity, item_price, item_id))
        conn.commit()
        flash('Data updated successfully!!!', 'success')
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM inventory')  # Fetch all items for dropdown
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('update_item.html', items=items)  # Pass all items



@app.route('/delete_item', methods=['GET','POST'])
def delete_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_sql_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        item_id  = request.form['item_id']
        cursor.execute('DELETE FROM inventory WHERE item_id = %s', (item_id,))
        conn.commit()
        flash('Item deleted successfully!!!', 'success')
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('delete_item.html', items = items)


if __name__ == "__main__":
    app.run(debug=True)