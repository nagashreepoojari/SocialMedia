from http.client import HTTPException

from flask import jsonify, request
from random import randrange
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError

from .database import app
from .models import db, Post, User
from . import schemas

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return {"message": "Hello, World!!!"}


@app.route("/posts", methods=['GET'])
def get_all_posts():
    try:
        posts = Post.query.all()
        result = [schemas.PostResponse.from_orm(post).dict() for post in posts]
        return jsonify(result), HTTPStatus.OK
    except SQLAlchemyError as e:
        # Handle database-related errors
        return jsonify({"error": "Database error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    except HTTPException as e:
        # Handle other HTTP-related errors
        return jsonify({"error": "HTTP error occurred", "message": e.description}), e.code
    except Exception as e:
        # Handle all other exceptions
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/posts", methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        post_data = schemas.PostCreate(**data)
        new_post_data = Post(
            id=randrange(0, 100000),
            title=post_data.title,
            content=post_data.content,
            published=post_data.published
        )

        db.session.add(new_post_data)
        db.session.commit()
        new_post = schemas.PostResponse.from_orm(new_post_data).dict()
        return jsonify(new_post), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/posts/<int:id>", methods=['GET'])
def read_post(id):
    try:
        post_data = Post.query.get(id)
        if post_data is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        post = schemas.PostResponse.from_orm(post_data).dict()
        return jsonify(post), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    try:
        post = Post.query.get(id)
        if post is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": f"Post with id:{id} was deleted"}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/posts/<int:id>", methods=['PUT'])
def update_post(id):
    try:
        data = request.get_json()
        post_data = schemas.PostUpdate(**data)
        post = Post.query.get(id)
        if post is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND

        post.title = post_data.title
        post.content = post_data.content
        post.published = post_data.published

        db.session.commit()
        return jsonify(post.to_dict()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/users", methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        # result = [schemas.PostResponse.from_orm(post).dict() for post in posts]
        result = [schemas.UserResponse.from_orm(user).dict() for user in users]
        return jsonify(result), HTTPStatus.OK
    except SQLAlchemyError as e:
        # Handle database-related errors
        return jsonify({"error": "Database error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    except HTTPException as e:
        # Handle other HTTP-related errors
        return jsonify({"error": "HTTP error occurred", "message": e.description}), e.code
    except Exception as e:
        # Handle all other exceptions
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/users", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user_data = schemas.UserCreate(**data)
        print(user_data.email)
        new_user_data = User(
            id=randrange(0, 100000),
            email=user_data.email,
            password=user_data.password
        )
        print(new_user_data)
        db.session.add(new_user_data)
        db.session.commit()
        new_user = schemas.UserResponse.from_orm(new_user_data).dict()
        return jsonify(new_user), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/users/<int:id>", methods=['GET'])
def read_user(id):
    try:
        user_data = User.query.get(id)
        if user_data is None:
            return jsonify({"message": f"User with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        user = schemas.UserResponse.from_orm(user_data).dict()
        return jsonify(user), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/users/<int:id>", methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return jsonify({"message": f"User with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User with id:{id} was deleted"}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/users/<int:id>", methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        user_data = schemas.UserUpdate(**data)
        user = User.query.get(id)
        if user is None:
            return jsonify({"message": f"User with id:{id} was not found"}), HTTPStatus.NOT_FOUND

        user.email = user_data.email
        user.password = user_data.password

        db.session.commit()
        return jsonify(user.to_dict()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
