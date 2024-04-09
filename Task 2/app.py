from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt
import requests
import json
import threading
from socket import gaierror, gethostbyname
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
from time import gmtime, strftime
#Importing all the libraries needed


app = Flask(__name__)
bcrypt = Bcrypt(app) # creates new bcrypt instance
app.config['SECRET_KEY'] = 'thisIsSecret'
login_manager = LoginManager(app)
login_manager.login_view="login_post"

#creates a user model representing the user
class User(UserMixin):
    def __init__ (self,id,email,password):
        self.id = id
        self.email = email
        self.password = password
        self.authenticated = False
        def is_active(self):
            return self.is_active()
        def is_anonymous(self):
            return False
        def is_authenticated(self):
            return self.authenticated
        def is_active(self):
            return True
        def get_id(self):
            return self.id
        def get_email(self):
            return self.email
        

@app.route('/login', methods =['POST', 'GET'])
def login_post():
    print("login post")
    if request.method=="GET":
        return render_template('login.html')
    print("login post 2")
    #check if alreddy logged in - if so send home
    if current_user.is_authenticated:
        print("already logged in")
        return redirect(url_for('bookings'))
        #standard database stuff and find the user with email
    con = sqlite3.connect("zoo.db")
    curs = con.cursor()
    email = request.form['email']
    curs.execute ("SELECT * FROM users where email = (?)",[email])
    #returns first matching user then pass the details to create a user object - unless there is nothing returned then flash a msg
    row = curs.fetchone()
    print(row)
    if row == None:
        flash('Please try logging in again')
        return render_template('login.html')
    user = list(row)
    liUser = User(int(user[0]),user[1],user[2])
    password = request.form['password']
    match = bcrypt.check_password_hash(liUser.password,password)
    #if mour password matches - run the login_user method 
    if match and email == liUser.email:
        login_user(liUser,remember=request.form.get('remember'))
        print("Home")
        return redirect(url_for('bookings'))
    else:
        flash('Pleae try logging in again')
        return render_template('login.html')
    return render_template('login.html')

@login_manager.user_loader
def load_user(id):
    conn = sqlite3.connect('zoo.db')
    curs = conn.cursor()
    curs.execute("SELECT * from users where id=(?)",[id])
    liUser = curs.fetchone()
    if liUser is None:
        return None
    else: 
        return User(int(liUser[0]), liUser[1], liUser[2])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    # Check if authenticated
    if current_user.is_authenticated:
        return redirect(url_for('bookings'))
    
    con = sqlite3.connect("zoo.db")
    curs = con.cursor()
    email = request.form['email']
    password = request.form['password']
    # We use bcrypt to hash the password we've put in with salt
    hashedPassword = bcrypt.generate_password_hash(password)
    # Now add the hashed pw to the db
    con.execute('insert into users(email,password) VALUES (?,?)',[email,hashedPassword])
    con.commit()
    return render_template('bookings.html')


@app.route('/bookings')
@login_required
def bookings():
    return render_template('bookings.html')
# Creates route for bookings

@app.route('/')
def home():
    return render_template('home.html')
# Creates route for index


@app.route('/Testimonials')
def testimonials():
    return render_template('testimonials.html')
#Route for testi;s

@app.route('/ouranimals')
def ouranimals():
    return render_template('ouranimals.html')
#Route for ouranimals

@app.route('/ot')
def openingtimes():
    return render_template('ot.html')
#Route for opening times

@app.route('/contactus', methods = ['POST', 'GET'])
def contactus():
    if request.method == 'POST':
        try: 
            flag=True
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone'] # requests the data from the from on the html
            message = request.form['message']
            

            if name =="" or email=="" or phone=="" or message=="" :
                msg = "Fail - cannot be blank"
                print("fail")
                flag=False # forces the website to not let it be blank

            else:          
                con = sqlite3.connect("zoo.db")
                cur = con.cursor()
                cur.execute("INSERT INTO contacts (name,email,phone,message) VALUES (?,?,?,?)", (name,email,phone,message))
                con.commit() # connects to the database and puts the data in the correct places
                msg = "Success, thank you for contacting us, we will get back with you as soon as we can."
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            if flag:
                con.close()
            return render_template("result.html", msg = msg) # gives the outcome on a seperate html
            
    return render_template("contactus.html")        




if __name__ == '__main__':
    app.run(debug=True)
#runs file
