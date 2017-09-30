from flask import redirect, render_template, session, request, flash
from app import app, db

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
