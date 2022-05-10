import flask

from . import db_session
from .users import User
from flask import jsonify, request


blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'about', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': news.to_dict(only=(
                'name', 'about', 'email'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'about', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        name=request.json['name'],
        about=request.json['about'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    if 'name' in request.json:
        user.name = request.json['name']
    if 'about' in request.json:
        user.about = request.json['about']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'hashed_password' in request.json:
        user.hashed_password = request.json['hashed_password']
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})