from core.extensions import db

def update(object):
    try:
        obj_merged = db.session.merge(object)
        db.session.commit()
        db.session.refresh(obj_merged)
        return obj_merged
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour : {e}")
        return None
    finally:
        db.session.close()