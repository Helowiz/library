from flask.cli import FlaskGroup

from app import db, app
from app.models.book import Book
from app.models.author import Author
from app.models.edition import Edition
from app.models.publisher import Publisher
from app.models.saga import Saga
from app.models.wrote import Wrote
from datetime import date

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
    new_saga = Saga(name="Harry Potter", volumes=7)
    new_book = Book(
        isbn=9780747532743,
        title="Harry Potter and the Philosopher's Stone",
        pages=223,
        summary="A young wizard discovers his magical heritage.",
        id_saga=1  # ID de la saga "Harry Potter" déjà ajoutée
    )
    new_author = Author(name="J.K. Rowling")
    new_relation = Wrote(isbn=9780747532743, id_author=1)
    new_publisher = Publisher(name="Penguin Books", language="English")
    new_edition = Edition(
        isbn=9780747532743,
        id_publisher=1,
        price=8,
        year_edition=date(1997, 6, 26)  # Date de publication
    )

    db.session.add_all([new_saga, new_book, new_author, new_relation, new_publisher, new_edition])
    db.session.commit()

if __name__ == "__main__":
    cli()
