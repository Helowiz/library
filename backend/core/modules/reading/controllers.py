from flask import Blueprint, jsonify
from .services import ReadingService
from .schemas import ReadingSchema

books_bp = Blueprint("reading", __name__, url_prefix='/reading')

### READ ###

@books_bp.route('/<int:id>', methods=['GET'])
def get_reading(id):
    book = ReadingService.get_book_by_id()
    return jsonify(ReadingSchema(many=True).dump(book))

### CREATE ###

@books_bp.route('/', methods=['POST'])
def start_reading():
    # TO DO
    pass

### UPDATE ###

@books_bp.route('/', methods=['PUT'])
def update_reading():
    # TO DO
    pass

### DELETE ###

@books_bp.route('/<int:id>', methods=['DELETE'])
def delete_reading(id):
    # TO DO
    pass
