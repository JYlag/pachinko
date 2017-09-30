from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User
from hashutils import check_pw_hash

def get_Users():
    return User.query.filter_by().all()

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
        username_db_count = User.query.filter_by(username=username).count()
        if len(password) < 3 or len(username) < 3:
            flash("Username and password must be more than 3 characters long")
            return redirect('/signup')
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/index")
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
