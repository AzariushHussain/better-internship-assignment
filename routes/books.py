from flask import request
from flask_restx import Namespace, Resource, fields
from models import Book, db
from utils.auth import token_required
from utils.pagination import paginate

books_ns = Namespace('books', description="Operations related to books")

book_model = books_ns.model('Book', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a book'),
    'title': fields.String(required=True, description='The title of the book'),
    'author': fields.String(required=True, description='The author of the book'),
    'published_date': fields.String(description='The published date of the book'),
})

create_book_model = books_ns.model('CreateBook', {
    'title': fields.String(required=True, description='The title of the book'),
    'author': fields.String(required=True, description='The author of the book'),
    'published_date': fields.String(description='The published date of the book'),
})

pagination_model = books_ns.model('PaginatedBooks', {
    'items': fields.List(fields.Nested(book_model)),
    'total': fields.Integer(description='Total number of books'),
    'pages': fields.Integer(description='Total number of pages'),
    'page': fields.Integer(description='Current page number'),
})

@books_ns.route('')
class BookList(Resource):
    @books_ns.doc('list_books')
    @books_ns.param('search', 'Search for books by title or author')
    @books_ns.param('page', 'Page number for pagination')
    @books_ns.param('per_page', 'Number of results per page')
    @books_ns.marshal_with(pagination_model)
    @token_required
    def get(self):
        """Get a list of books"""
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = Book.query
        if search:
            query = query.filter((Book.title.contains(search)) | (Book.author.contains(search)))
        books = query.all()

        resp = paginate(books, page, per_page)
        return resp, 200

    @books_ns.doc('create_book')
    @books_ns.expect(create_book_model, validate=True)
    @books_ns.marshal_with(book_model, code=201)
    @token_required
    def post(self):
        """Add a new book"""
        data = request.json
        new_book = Book(title=data['title'], author=data['author'], published_date=data.get('published_date'))
        db.session.add(new_book)
        db.session.commit()
        return new_book, 201

@books_ns.route('/<int:id>')
@books_ns.param('id', 'The book identifier')
class BookResource(Resource):
    @books_ns.doc('get_book')
    @books_ns.marshal_with(book_model)
    @token_required
    def get(self, id):
        """Get a specific book by its ID"""
        book = Book.query.get_or_404(id)
        return book, 200

    @books_ns.doc('update_book')
    @books_ns.expect(create_book_model, validate=True)
    @books_ns.marshal_with(book_model)
    @token_required
    def put(self, id):
        """Update a book by its ID"""
        book = Book.query.get_or_404(id)
        data = request.json
        book.title = data['title']
        book.author = data['author']
        book.published_date = data.get('published_date', book.published_date)
        db.session.commit()
        return book, 200

    @books_ns.doc('delete_book')
    @token_required
    def delete(self, id):
        """Delete a book by its ID"""
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return '', 204  
