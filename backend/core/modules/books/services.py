from .repositories import BookRepository

class BookService:
    @staticmethod
    def get_all_books():
        books = BookRepository.get_all()
        return sorted(books, key=lambda b: b.title)

    @staticmethod
    def get_book_by_id(id):
        return BookRepository.get_by_id(id)

    @staticmethod
    def create_book(data):
        book_data = data["book"]
        authors_data = data["authors"]
        return BookRepository.create(book_data, authors_data)

    @staticmethod
    def update_book(id, book_data):
        return BookRepository.update(id, book_data)

    @staticmethod
    def delete_book(id):
        deleted_book = BookRepository.get_by_id(id)
        if BookRepository.delete(id):
            return deleted_book
        return None
