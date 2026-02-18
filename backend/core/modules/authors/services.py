from .repositories import AuthorRepository


class AuthorService:
    @staticmethod
    def get_all_authors():
        authors = AuthorRepository.get_all()
        return sorted(authors, key=lambda b: b.name)

    @staticmethod
    def get_author_by_id(id):
        author = AuthorRepository.get_by_id(id)
        return author

    @staticmethod
    def get_author_by_title(title):
        author = AuthorRepository.get_by_name(title)
        return author

    @staticmethod
    def create_author(data):
        author = AuthorRepository.create(data["author"])
        return author

    @staticmethod
    def update_author(id, data):
        return AuthorRepository.update(id, data)

    @staticmethod
    def delete_author(id):
        author = AuthorRepository.get_by_id(id)
        AuthorRepository.delete(id)
        return author
