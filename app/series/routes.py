from app.series import bp
from app.models.book import Series, SeriesStatus, Book
from flask import render_template
from app.extensions import db

@bp.route("/")
def list_series():
    series_list = Series.query.all()

    rows = db.session.query(Book.series_id, Book.series_volume)\
    .filter(Book.series_id.isnot(None))\
    .filter(Book.series_volume.isnot(None))\
    .order_by(Book.series_volume)\
    .all()
    
    volumes_by_series = {}
    for series_id, volume in rows:
        if series_id not in volumes_by_series:
            volumes_by_series[series_id] = []
    volumes_by_series[series_id].append(volume)

    return render_template("series/list.html", series_list=series_list, SeriesStatus=SeriesStatus, owned_volumes=volumes_by_series)

@bp.route("/<int:series_id>")
def detail_series(series_id):
    series = Series.query.get_or_404(series_id)
    return render_template("series/detail.html", series=series)