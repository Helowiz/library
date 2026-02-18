from core.extensions import db

def insert(object):
    try:
        db.session.add(object)
        db.session.commit()
        db.session.refresh(object)
        return object
    except Exception as e:
        db.session.rollback()
        print(e)
        return None
    finally:
        db.session.close()