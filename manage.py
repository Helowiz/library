from flask.cli import FlaskGroup

from app import app, db
from app.models.book import Book

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Book(title="Nevernight", author="Jay Kristoff"))
    db.session.commit()

if __name__ == "__main__":
    cli()
