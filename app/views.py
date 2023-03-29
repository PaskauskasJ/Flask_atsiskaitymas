from app import app
from flask import render_template, request, redirect, flash, url_for
from datetime import datetime

app.config['SECRET_KEY'] = 'fhadkjhakjfdh'


@app.route('/')
def index():
    # return render_template('public/index.html', title="Pradžia", title2="JAV populiariausias sportas")
    date = datetime.utcnow()


date = datetime.utcnow()
