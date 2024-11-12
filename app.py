from flask import Flask, render_template, request, url_for, redirect, flash, session
import mysql.connector
from time import sleep
from date_calc import *

app = Flask(__name__, template_folder="f_templates")
app.secret_key = "77d48e2e153c7796b4bdd39598f9935b6165f26ff8e1eb3b"

@app.before_request
def initialize_session():
    if 'username' not in session:
        session['username'] = None
    if 'userid' not in session:
        session['userid'] = None

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="pfa_orange"
)

cursor = db.cursor()

def login_required(f):
    def decorated_function(*args, **kwargs):
        if session.get('username') is None or session.get('userid') is None:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route("/")
def index():
    userid = session.get('userid')
    cursor.execute('SELECT * FROM user_details WHERE User_ID = %s', (userid,))
    query = cursor.fetchall()
    return render_template('homepage.html', query=query)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('SELECT User_ID, Pwd, User_name FROM user_details WHERE User_ID = %s', (username,))
        user = cursor.fetchone()
        if user and user[1] == password:  
            session['username'] = user[2]  
            session['userid'] = user[0]
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route("/schemes")
def schemes():
    return redirect("http://127.0.0.1:3000/schemes")

   
@app.route("/forgot_pwd", methods=['GET', 'POST'])
def forgot_pwd():
    if request.method == 'GET':
        return render_template('forgot_pwd.html')
    elif request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        cursor.execute('UPDATE user_details SET pwd = %s WHERE user_id = %s', (new_password, username))
        db.commit()
        return redirect(url_for('login'))

@app.route("/admin",methods=['GET','POST'])
def admin():
    if request.method=="GET":
        return render_template("admin.html")
    elif request.method=="POST":
        admin_name=request.form['admin_name']
        password=request.form['pass_wd']
        user_id=request.form['user_id']
        print(admin_name,password,user_id)
        return render_template("admin.html")
    
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        conf_pwd = request.form['confirm_password']
        acc_number = request.form['acc_number']
        ifsc = request.form['ifsc']
        pan = request.form['pan']
        status = request.form['status']
        acc_type = request.form['acc_type']
        created_on = request.form['created_on']
        if password == conf_pwd:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO user_details (user_id, user_name, mob, email_id, dob, pwd) VALUES (%s, %s, %s, %s, %s, %s)''', (user_id, name, mobile, email, dob, password))
            cursor.execute('''INSERT INTO account_details (acc_no, ifsc, pan, acc_status, acc_type, acc_create, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (acc_number, ifsc, pan, status, acc_type, created_on, user_id))
            db.commit()
        else:
            return redirect(url_for('signup'))
        return redirect(url_for('login'))
    
@app.route("/savings", methods=['GET', 'POST'])
@login_required
def savings():
    if request.method == 'GET':
        return render_template('savings.html')
    elif request.method == 'POST':
        trans_id = request.form['trans_id']
        user_id = request.form['user_id']
        scheme_id = request.form['scheme_id']
        amount = request.form['amount']

        cursor.execute(f'''
            SELECT user_details.Mob, account_details.acc_no, account_details.pan 
            FROM user_details 
            JOIN account_details 
            ON user_details.User_ID = account_details.user_id 
            WHERE user_details.User_ID = %s
        ''', (user_id,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute('SELECT calc_int_amt(%s, %s)', (amount, scheme_id))
            mat_amt = cursor.fetchone()[0]
            mat_date = maturity_date(int(scheme_id))
            
            cursor.execute('''
                INSERT INTO savings_details 
                (user_id_savings, account_number, mobile_number, Scheme_ID, amount, pan, Maturity_Amount, invested_date, Maturity_Date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, result[1], result[0], scheme_id, amount, result[2], mat_amt, mat_date[0], mat_date[1]))
            
            db.commit()
            
            cursor.execute('''
                INSERT INTO transactions
                (Transaction_ID, User_ID, Debit_Amount, Debit_Date, Credit_Amount, Credit_Date) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (trans_id, user_id, amount, mat_date[0], mat_amt, mat_date[1]))
            
            db.commit()
            return redirect(url_for('schemes'))
        else:
            flash("User details not found. Please try again.", "warning")
            return redirect(url_for("savings"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)