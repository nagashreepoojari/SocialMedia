from http.client import HTTPException

from flask import jsonify, request
from random import randrange
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError

from .database import app
from .models import db, Post

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return {"message": "Hello, World!!!"}


@app.route("/posts", methods=['GET'])
def get_all_posts():
    try:
        posts = Post.query.all()
        result = [post.to_dict() for post in posts]
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
        new_post = Post(
            id=randrange(0, 100000),
            title=data.get('title'),
            content=data.get('content'),
            published=data.get('published')  # Default to True if not provided
        )

        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.to_dict()), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/posts/<int:id>", methods=['GET'])
def read_post(id):
    try:
        post = Post.query.get(id)
        if post is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        return jsonify(post.to_dict()), HTTPStatus.OK
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
        post = Post.query.get(id)
        if post is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND

        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        post.published = data.get('published', post.published)

        db.session.commit()
        return jsonify(post.to_dict()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
