from flask import render_template
from app.book import bp

@bp.route('/')
def index():
    return render_template('book/index.html')

@bp.route('/add/')
def add():
    return render_template('book/add.html')

@bp.route('/delete/')
def delete():
    return render_template('book/delete.html')

@bp.route('/update/')
def update():
    return render_template('book/update.html')
