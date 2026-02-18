from .models import Book
from core.modules.authors.repositories import AuthorRepository
from core.repositories.insert import insert
from core.repositories.update import update
from core.repositories.delete import delete


class BookRepository:
    @staticmethod
    def get_all():
        return Book.query.all()

    @staticmethod
    def get_by_id(id):
        return Book.query.get(id)

    @staticmethod
    def create(book_data, authors_data):
        new_book = Book(
            title=book_data["title"],
            synopsis=book_data["synopsis"],
            isbn=book_data["isbn"],
            cover_url=book_data["cover_url"],
            publisher=book_data["publisher"],
            language=book_data["language"],
            number_of_pages=book_data["number_of_pages"],
            format=book_data["format"],
        )

        for author in authors_data:
            new_author = AuthorRepository.get_by_name(author["name"])

            if not new_author:
                new_author = AuthorRepository.create(author)

            new_book.authors.append(new_author)

        return insert(new_book)

    @staticmethod
    def update(id, data):
        book = Book.query.get(id)
        if not book:
            return None
        
        for key, value in data.items():
            setattr(book, key, value)
        return update(book)
        

    @staticmethod
    def delete(id):
        book = Book.query.get(id) 
        return delete(book)
        
