from .models import Author

from core.repositories.insert import insert
from core.repositories.update import update
from core.repositories.delete import delete

class AuthorRepository:
    @staticmethod
    def get_all():
        return Author.query.all()

    @staticmethod
    def get_by_id(id):
        return Author.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Author.query.filter_by(name=name).first()

    @staticmethod
    def create(data):
        new_author = Author(
            name=data['name']
            )
        return insert(new_author)

    @staticmethod
    def update(id, data):
        author = Author.query.get(id)
        if not author:
            return None
        
        for key, value in data.items():
            setattr(author, key, value)
        return update(author)

    @staticmethod
    def delete(id):
        author = Author.query.get(id) 
        return delete(author)
