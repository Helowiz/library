from app.series import bp
from app.models.book import Series 
from flask import render_template

@bp.route("/")
def list_series():
    series_list = Series.query.all()
    return render_template("series/list.html", series_list=series_list)