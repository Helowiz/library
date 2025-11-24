import random
from datetime import datetime, timedelta
from faker import Faker
from app import create_app  # Assure-toi que ta factory function est bien importée
from app.extensions import db

# Adapte ces imports selon l'endroit où sont tes fichiers models
from app.models.book import (
    Author, Series, Tag, Book, Quote,
    FormatType, SeriesStatus
)

from app.models.planning import (
    MonthlyPAL, MonthlyBookSelection
)


from app.models.reading import (
    ReadingSession, ReadingStatus
)
# Initialisation de Faker en français
fake = Faker(['fr_FR'])

def seed_database():
    # Création du contexte d'application Flask
    app = create_app()
    
    with app.app_context():
        print("🗑️  Nettoyage de la base de données...")
        db.drop_all()
        db.create_all()

        print("🌱 Création des données de test...")

        # --- 1. Création des Tags (Genres) ---
        genres = [
            "Fantasy", "Science-Fiction", "Thriller", "Romance", "Horreur", 
            "Policier", "Historique", "Développement personnel", "Biographie", "Manga"
        ]
        tags_objects = []
        for genre in genres:
            tag = Tag(name=genre)
            tags_objects.append(tag)
            db.session.add(tag)
        
        db.session.commit()
        print(f"✅ {len(genres)} genres ajoutés.")

        # --- 2. Création des Auteurs ---
        authors_objects = []
        for _ in range(20):
            author = Author(name=fake.name())
            authors_objects.append(author)
            db.session.add(author)
        
        db.session.commit()
        print(f"✅ {len(authors_objects)} auteurs ajoutés.")

        # --- 3. Création des Séries ---
        series_objects = []
        for _ in range(10):
            series = Series(
                title=fake.sentence(nb_words=3).replace(".", ""),
                nb_of_volumes=random.randint(3, 12),
                status=random.choice(list(SeriesStatus))
            )
            series_objects.append(series)
            db.session.add(series)
        
        db.session.commit()
        print(f"✅ {len(series_objects)} séries ajoutées.")

        # --- 4. Création des Livres ---
        books_objects = []
        
        # Formats possibles
        formats = list(FormatType)

        for _ in range(50): # Créons 50 livres
            # Choix aléatoire d'un auteur
            author = random.choice(authors_objects)
            
            # 50% de chance d'être dans une série
            is_in_series = random.choice([True, False])
            selected_series = None
            volume_num = None
            
            if is_in_series:
                selected_series = random.choice(series_objects)
                volume_num = random.randint(1, selected_series.nb_of_volumes)

            # Création du livre
            book = Book(
                title=fake.sentence(nb_words=4).replace(".", ""),
                synopsis=fake.paragraph(nb_sentences=5),
                isbn=fake.isbn13().replace("-", ""),
                cover_url=f"https://picsum.photos/seed/{random.randint(1,1000)}/200/300", # Image aléatoire
                publisher=fake.company(),
                language="FR",
                number_of_pages=random.randint(150, 900),
                format=random.choice(formats),
                author_id=author.id,
                series_id=selected_series.id if selected_series else None,
                series_volume=volume_num,
                added_at=fake.date_time_between(start_date='-2y', end_date='now')
            )

            # Ajout de 1 à 3 tags aléatoires
            book.tags.extend(random.sample(tags_objects, k=random.randint(1, 3)))

            books_objects.append(book)
            db.session.add(book)

        db.session.commit()
        print(f"✅ {len(books_objects)} livres ajoutés.")

        # --- 5. Création des Citations (Quotes) ---
        for book in random.sample(books_objects, 15): # Ajoute des citations à 15 livres
            quote = Quote(
                content=fake.sentence(nb_words=15),
                page_number=random.randint(10, book.number_of_pages or 100),
                book_id=book.id
            )
            db.session.add(quote)
        
        print("✅ Citations ajoutées.")

        # --- 6. Création des Sessions de Lecture ---
        # Pour chaque livre, on décide s'il a été lu ou non
        reading_statuses = list(ReadingStatus)
        
        for book in books_objects:
            # 70% de chance d'avoir une entrée dans le journal de lecture
            if random.random() > 0.3:
                status = random.choice(reading_statuses)
                
                start_date = fake.date_between(start_date='-1y', end_date='today')
                finish_date = None
                rating = None
                review = None
                current_page = 0

                if status == ReadingStatus.READ:
                    finish_date = start_date + timedelta(days=random.randint(2, 30))
                    rating = random.randint(1, 5)
                    review = fake.paragraph(nb_sentences=3)
                    current_page = book.number_of_pages
                elif status == ReadingStatus.READING:
                    current_page = random.randint(1, book.number_of_pages or 100)
                
                session = ReadingSession(
                    book_id=book.id,
                    status=status,
                    start_date=start_date,
                    finish_date=finish_date,
                    current_page=current_page,
                    rating=rating,
                    review=review,
                    is_reread=random.choice([True, False])
                )
                db.session.add(session)

        print("✅ Sessions de lecture ajoutées.")

        # --- 7. Création d'une PAL Mensuelle (Monthly PAL) ---
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        pal = MonthlyPAL(
            month=current_month,
            year=current_year,
            theme="Lectures d'Automne" if current_month in [9, 10, 11] else "Lectures du moment"
        )
        db.session.add(pal)
        db.session.commit() # Commit pour avoir l'ID de la PAL

        # Sélectionner 3 livres au hasard pour la PAL
        pal_books = random.sample(books_objects, 3)
        for index, book in enumerate(pal_books):
            selection = MonthlyBookSelection(
                monthly_pal_id=pal.id,
                book_id=book.id,
                priority=index + 1,
                note=fake.sentence(nb_words=5)
            )
            db.session.add(selection)

        db.session.commit()
        print(f"✅ PAL mensuelle créée pour {current_month}/{current_year}.")

        print("🚀 Base de données remplie avec succès !")

if __name__ == "__main__":
    seed_database()