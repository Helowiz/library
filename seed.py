import csv
import os
from app import create_app, db
from app.models.book import Book, Author, Series, FormatType
from app.models.reading import ReadingSession, ReadingStatus

# Initialisation
app = create_app()

def get_or_create_author(name):
    """Récupère ou crée un auteur."""
    if not name: return None
    clean_name = name.strip()
    author = Author.query.filter_by(name=clean_name).first()
    if not author:
        author = Author(name=clean_name)
        db.session.add(author)
        db.session.commit()
    return author

def get_or_create_series(title):
    """Récupère ou crée une série."""
    if not title: return None
    clean_title = title.strip()
    series = Series.query.filter_by(title=clean_title).first()
    if not series:
        series = Series(title=clean_title)
        db.session.add(series)
        db.session.commit()
    return series

def safe_int(value, default=0):
    """Convertit en int sans planter."""
    try:
        return int(value) if value else default
    except ValueError:
        return default

def safe_float(value, default=0.0):
    """Convertit en float sans planter (gère 1.5 et 1,5)."""
    try:
        if not value: return default
        return float(value.replace(',', '.'))
    except ValueError:
        return default

def map_status(status_str):
    """Mappe le statut CSV vers l'Enum."""
    status_str = status_str.upper().strip() if status_str else ""
    mapping = {
        "READ": ReadingStatus.READ,
        "READING": ReadingStatus.READING,
        "DNF": ReadingStatus.DNF,
        "PAUSE": ReadingStatus.PAUSE,
        "WISHLIST": ReadingStatus.WISHLIST,
        "TBR": ReadingStatus.TBR
    }
    
    return mapping.get(status_str, ReadingStatus.TBR)

def import_books():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data', 'books.csv')
    
    with app.app_context():
        print("\n🌱 DÉBUT DU SEEDING AVEC GESTION D'ERREURS...")
        
        try:
            with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                
                success_count = 0
                skip_count = 0
                error_count = 0
                
                for row_index, row in enumerate(reader, start=2): # start=2 car ligne 1 = headers
                    try:
                        # --- 1. Nettoyage et Récupération des Données ---
                        title = row.get('title', '').strip()
                        author_name = row.get('author', '').strip()
                        
                        if not title or not author_name:
                            print(f"   ⚠️  Ligne {row_index}: Titre ou Auteur manquant. Ignorée.")
                            error_count += 1
                            continue

                        # --- 2. Gestion Auteur ---
                        author_obj = get_or_create_author(author_name)

                        # --- 3. Vérification Doublon ---
                        existing = Book.query.filter_by(title=title, author_id=author_obj.id).first()
                        if existing:
                            print(f"   ⏭️  Ligne {row_index}: '{title}' existe déjà.")
                            skip_count += 1
                            continue

                        # --- 4. Gestion Série (Saga) ---
                        series_title = row.get('series', '').strip() # ex: "Harry Potter"
                        series_obj = get_or_create_series(series_title)
                        
                        series_vol = safe_float(row.get('volume')) # ex: 1.5

                        # --- 5. Création du Livre ---
                        new_book = Book(
                            title=title,
                            synopsis=row.get('synopsis', 'Pas de résumé'),
                            cover_url=row.get('cover_url', ''),
                            number_of_pages=safe_int(row.get('pages')),
                            
                            # Relations
                            author=author_obj,
                            series=series_obj,
                            series_volume=series_vol,
                            
                            # Défauts
                            language="FR",
                            format=FormatType.PAPIER
                        )

                        # --- 6. Gestion Lecture ---
                        reading_status = map_status(row.get('status'))
                        current_page = safe_int(row.get('current_page'))
                        
                        # Logique intelligente pour la page
                        if reading_status == ReadingStatus.READ:
                            current_page = new_book.number_of_pages or 0

                        session = ReadingSession(
                            book=new_book,
                            status=reading_status,
                            current_page=current_page
                        )
                        new_book.readings.append(session)

                        # --- 7. Sauvegarde ---
                        db.session.add(new_book)
                        success_count += 1
                        
                        # Feedback visuel console
                        series_info = f" [Série: {series_obj.title} #{series_vol}]" if series_obj else ""
                        print(f"   ✅ Ajouté : {title}{series_info}")

                    except Exception as e_row:
                        # Si une ligne plante, on l'affiche mais on ne stoppe pas le script
                        print(f"   ❌ ERREUR CRITIQUE Ligne {row_index} ({title}): {e_row}")
                        db.session.rollback() # On annule juste cette transaction
                        error_count += 1

            # Commit final
            db.session.commit()
            print("-" * 40)
            print(f"Rapport : ✅ {success_count} ajoutés | ⏭️ {skip_count} passés | ❌ {error_count} erreurs")

        except FileNotFoundError:
            print(f"❌ Erreur Fatale : Fichier introuvable à {csv_file_path}")

if __name__ == '__main__':
    import_books()