from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User
from hashutils import check_pw_hash

def get_Users():
    return User.query.filter_by().all()

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
        return redirect("/newblog")
    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run()
