from flask import redirect, render_template, session, request, flash
from app import app, db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def runGame():
    return render_template('game.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
