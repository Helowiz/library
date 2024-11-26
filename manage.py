from flask.cli import FlaskGroup

from app import db, app
from app.models.book import Book

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    print(f"Connecting to database: {db.engine.url}")

    db.drop_all()
    db.create_all()
    db.session.commit()

    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables created: {tables}")

@cli.command("seed_db")

def seed_db():
    db.session.commit()

if __name__ == "__main__":
    cli()
