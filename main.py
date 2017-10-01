from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User
from hashutils import check_pw_hash

def get_Users():
    return User.query.filter_by().all()

def input_is_valid(text):
    return len(text) >= 3 and len(text) <= 20

def verify_passwords(password,verify_pass):
    return password == verify_pass

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'contact']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def runGame():
    return render_template('game.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:

            if not input_is_valid(username):
                flash("Username does not meet requirements. Please enter a different user", "error")
            if not input_is_valid(password):
                flash("Password does not meet requirements. Please try again.", "error")
            if not verify_passwords(password, verify):
                flash("Passwords do not match. Please try again.", "error")

            if input_is_valid(username) and input_is_valid(password) and verify_passwords(password,verify):
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['user'] = username
                return redirect('/game')

            return redirect('/signup')
        else:
            flash("Username already exists! Enter a different username", "error")
            return redirect('/signup')
    else:
        return render_template('signup.html')

@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['user'] = user.username
            flash("Logged In!")
            return redirect("/game")
        else:
            flash("Username doesnt not exist, or password is incorrect.", "error")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    del session['user']
    return redirect("/blog")


if __name__ == '__main__':
    app.run()
