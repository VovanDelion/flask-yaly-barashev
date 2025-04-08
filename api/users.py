import flask
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify({
        'users': [user.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position',
            'specialty', 'address', 'email', 'modified_date'
        )) for user in users]
    })


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = db_session.create_session()
    user = session.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({
        'user': user.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position',
            'specialty', 'address', 'email', 'modified_date'
        ))
    })


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

        required_fields = ['surname', 'name', 'email', 'password']
        if not all(field in request.json for field in required_fields):
            return make_response(jsonify({'error': 'Missing required fields'}), 400)

    session = db_session.create_session()
    if session.query(User).filter(User.email == request.json['email']).first():
        return make_response(jsonify({'error': 'Email already exists'}), 400)

        user = User(
            surname=request.json['surname'],
            name=request.json['name'],
            age=request.json.get('age'),
            position=request.json.get('position'),
            specialty=request.json.get('specialty'),
            address=request.json.get('address'),
            email=request.json['email']
        )
        user.set_password(request.json['password'])

        session.add(user)
        session.commit()

    return make_response(jsonify({
        'success': 'User created',
        'user_id': user.id
    }), 201)


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

        session = db_session.create_session()
        user = session.get(User, user_id)
        if not user:
            return make_response(jsonify({'error': 'Not found'}), 404)

    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'specialty' in request.json:
        user.specialty = request.json['specialty']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        if session.query(User).filter(User.email == request.json['email'], User.id != user_id).first():
            return make_response(jsonify({'error': 'Email already in use'}), 400)
            user.email = request.json['email']
            if 'password' in request.json:
                user.hashed_password = generate_password_hash(request.json['password'])

            user.modified_date = datetime.datetime.now()
            session.commit()

    return jsonify({
        'success': 'User updated',
        'user_id': user.id
    })


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    session.delete(user)
    session.commit()

    return make_response(jsonify({
        'success': 'User deleted',
        'user_id': user_id
    }), 200)
