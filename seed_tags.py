from app import create_app, db
from app.models.book import Tag

app = create_app()


def seed_tags():
    # Une liste complète de genres littéraires
    genres = [
        # --- Fiction ---
        "Fantasy",
        "Science-Fiction",
        "Dystopie",
        "Fantastique",
        "Thriller",
        "Policier",
        "Horreur",
        "Romance",
        "Aventure",
        "Historique",
        "Contemporain",
        "Classique",
        "Humour",
        "Drame",
        # --- Jeunesse / Graphique ---
        "Young Adult",
        "Jeunesse",
        "Manga",
        "Comics",
        "Bande Dessinée",
        "Roman Graphique",
        # --- Non-Fiction ---
        "Biographie",
        "Autobiographie",
        "Essai",
        "Développement Personnel",
        "Philosophie",
        "Psychologie",
        "Histoire",
        "Science",
        "Voyage",
        "Cuisine",
        "Art",
        "True Crime",
        # --- Formes ---
        "Poésie",
        "Théâtre",
        "Nouvelles",
    ]

    with app.app_context():
        print("🏷️  Début de l'ajout des Tags (Genres)...")
        added_count = 0

        for genre_name in genres:
            # On vérifie si le tag existe déjà pour ne pas faire planter le script
            existing_tag = Tag.query.filter_by(name=genre_name).first()

            if not existing_tag:
                new_tag = Tag(name=genre_name)
                db.session.add(new_tag)
                added_count += 1
                print(f"   ✅ Ajouté : {genre_name}")
            else:
                print(f"   ⚠️  Existe déjà : {genre_name}")

        try:
            db.session.commit()
            print("-" * 30)
            print(f"🎉 Terminé ! {added_count} nouveaux genres ajoutés.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de l'enregistrement : {e}")


if __name__ == "__main__":
    seed_tags()
