from flask import Blueprint, jsonify, request
from .services import BookService
from .schemas import BookSchema

books_bp = Blueprint("books", __name__)

### READ ###


@books_bp.route("/", methods=["GET"])
def get_books():
    books = BookService.get_all_books()
    return jsonify(BookSchema(many=True).dump(books)), 200


@books_bp.route("/<int:id>", methods=["GET"])
def get_book_by_id(id):
    book = BookService.get_book_by_id(id)
    if book:
        return jsonify(BookSchema(many=False).dump(book)), 200
    return {"error" : "Can't find that book"}


### CREATE ###


@books_bp.route("/", methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = BookService.create_book(data)
    if new_book:
        return jsonify(BookSchema().dump(new_book)), 201
    return {"error" : "An error occurred while creating the book"}


### UPDATE ###


@books_bp.route("/<int:id>", methods=["PUT"])
def update_book(id):
    data = request.get_json()
    updated_book = BookService.update_book(id, data)
    if updated_book:
        return jsonify(BookSchema().dump(updated_book)), 200
    return {"error" : "An error occurred while updating the book"}


### DELETE ###


@books_bp.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    deleted_book = BookService.delete_book(id)
    if deleted_book:
        return jsonify(BookSchema().dump(deleted_book)), 200
    return {"error" : "An error occured while deleting the book"}
