from core.extensions import db

def delete(object):
    try:
        obj_to_delete = db.session.merge(object)
        db.session.delete(obj_to_delete)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression : {e}")
        return False
    finally:
        db.session.close()