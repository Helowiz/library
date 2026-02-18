from flask import Blueprint, jsonify, request
from .services import AuthorService
from .schemas import AuthorSchema

authors_bp = Blueprint("authors", __name__)

### READ ###


@authors_bp.route("/", methods=["GET"])
def get_authors():
    authors = AuthorService.get_all_authors()
    return jsonify(AuthorSchema(many=True).dump(authors)), 200


@authors_bp.route("/<int:id>", methods=["GET"])
def get_author_by_id(id):
    author = AuthorService.get_author_by_id(id)
    if author :
        return jsonify(AuthorSchema(many=False).dump(author)), 200
    return {"error" : "Can't find this author"}


### CREATE ###


@authors_bp.route("/", methods=["POST"])
def add_author():
    author = request.get_json()
    new_author = AuthorService.create_author(author)
    return jsonify(AuthorSchema().dump(new_author)), 201


### UPDATE ###


@authors_bp.route("/<int:id>", methods=["PUT"])
def update_author(id):
    data = request.get_json()
    updated_author = AuthorService.update_author(id, data)
    return jsonify(AuthorSchema().dump(updated_author)), 200


### DELETE ###


@authors_bp.route("/<int:id>", methods=["DELETE"])
def delete_author(id):
    AuthorService.delete_author(id)
    return "", 204
