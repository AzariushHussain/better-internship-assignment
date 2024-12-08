from flask import request
from flask_restx import Namespace, Resource, fields
from models import Member, db
from utils.auth import token_required
from utils.pagination import paginate

members_ns = Namespace('members', description="Operations related to library members")

member_model = members_ns.model('Member', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a member'),
    'name': fields.String(required=True, description='The name of the member'),
    'email': fields.String(required=True, description='The email of the member'),
    'membership_date': fields.String(description='The date of membership registration'),
})

create_member_model = members_ns.model('CreateMember', {
    'name': fields.String(required=True, description='The name of the member'),
    'email': fields.String(required=True, description='The email of the member'),
    'membership_date': fields.String(description='The date of membership registration'),
})

pagination_model = members_ns.model('PaginatedMembers', {
    'items': fields.List(fields.Nested(member_model)),
    'total': fields.Integer(description='Total number of members'),
    'pages': fields.Integer(description='Total number of pages'),
    'page': fields.Integer(description='Current page number'),
})


@members_ns.route('')
class MemberList(Resource):
    @members_ns.doc('list_members')
    @members_ns.param('search', 'Search for members by name or email')
    @members_ns.param('page', 'Page number for pagination')
    @members_ns.param('per_page', 'Number of results per page')
    @members_ns.marshal_with(pagination_model)
    @token_required
    def get(self):
        """Get a list of members"""
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = Member.query
        if search:
            query = query.filter((Member.name.contains(search)) | (Member.email.contains(search)))
        
        members = query.all()

        resp = paginate(members, page, per_page)
        print("Paginated response:", resp)  
        return resp, 200


    @members_ns.doc('create_member')
    @members_ns.expect(create_member_model, validate=True)
    @members_ns.marshal_with(member_model, code=201)
    @token_required
    def post(self):
        """Add a new member"""
        data = request.json
        new_member = Member(name=data['name'], email=data['email'], membership_date=data.get('membership_date'))
        db.session.add(new_member)
        db.session.commit()
        return new_member, 201

@members_ns.route('/<int:id>')
@members_ns.param('id', 'The member identifier')
class MemberResource(Resource):
    @members_ns.doc('update_member')
    @members_ns.expect(create_member_model, validate=True)
    @members_ns.marshal_with(member_model)
    @token_required
    def put(self, id):
        """Update a member's details"""
        member = Member.query.get_or_404(id)
        
        data = request.json
        member.name = data['name']
        member.email = data['email']
        member.membership_date = data.get('membership_date', member.membership_date)
        
        db.session.commit()
        return member

    @members_ns.doc('delete_member')
    @token_required
    def delete(self, id):
        """Delete a member by ID"""
        member = Member.query.get_or_404(id)
        db.session.delete(member)
        db.session.commit()
        return '', 204  
