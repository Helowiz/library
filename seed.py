import csv
import os
from app import create_app, db
from app.models.book import Book
from app.models.reading import Reading, BookStatus

app = create_app()

def import_books():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data', 'books.csv')
    
    with app.app_context():
        print("🌱 Début de l'importation des données...")
        
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                
                added_count = 0
                skipped_count = 0
                
                for row in reader:
                    existing_book = Book.query.filter_by(title=row['title']).first()
                    
                    if existing_book:
                        print(f"   ⚠️  Existe déjà : {row['title']}")
                        skipped_count += 1
                        continue
                    
                    pages = int(row['pages']) if row['pages'] else 0
                    
                    new_book = Book(
                        title=row['title'],
                        author=row['author'],
                        synopsis=row['synopsis'],
                        cover_url=row['cover_url'],
                        number_of_pages=pages
                    )
                    
                    status_str = row['status']
                    current_page = int(row['current_page']) if row['current_page'] else 0
                    
                    status_enum = None
                    if status_str in BookStatus.__members__:
                        status_enum = BookStatus[status_str]
                    
                    reading_entry = Reading(
                        status=status_enum,
                        current_page=current_page
                    )
                    
                    new_book.reading_status = reading_entry
                    
                    db.session.add(new_book)
                    added_count += 1
                    print(f"   ✅ Ajouté : {row['title']} ({status_str})")
            
            db.session.commit()
            print("-" * 30)
            print(f"Terminé ! {added_count} livres ajoutés, {skipped_count} ignorés.")
            
        except FileNotFoundError:
            print(f"❌ Erreur : Le fichier {csv_file_path} est introuvable.")
        except Exception as e:
            print(f"❌ Une erreur est survenue : {e}")
            db.session.rollback()

if __name__ == '__main__':
    import_books()