from http import HTTPStatus
from http.client import HTTPException
from random import randrange

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app import schemas
from app.models import Post, db

posts_bp = Blueprint('posts_bp', __name__)


@posts_bp.route("/", methods=['GET'])
def get_all_posts():
    """
        Get All Posts
        ---
        responses:
          200:
            description: A list of all posts
          500:
            description: Database error occurred
    """
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


@posts_bp.route("/", methods=['POST'])
def create_post():
    """
        Create a New Post
        ---
        responses:
          201:
            description: Post created successfully
          500:
            description: Database error occurred
    """
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


@posts_bp.route("/<int:id>", methods=['GET'])
def read_post(id):
    """
       Get a Single Post
       ---
       parameters:
         - name: id
           in: path
           type: integer
           required: true
           description: The ID of the post to retrieve
       responses:
         200:
           description: Post found
         404:
    """
    try:
        post_data = Post.query.get(id)
        if post_data is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        post = schemas.PostResponse.from_orm(post_data).dict()
        return jsonify(post), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@posts_bp.route("/<int:id>", methods=['DELETE'])
def delete_post(id):
    """
        Delete a Post
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the post to delete
        responses:
          204:
            description: Post deleted
          404:
            description: Post not found
    """
    try:
        post = Post.query.get(id)
        if post is None:
            return jsonify({"message": f"Post with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": f"Post with id:{id} was deleted"}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@posts_bp.route("/<int:id>", methods=['PUT'])
def update_post(id):
    """
        Update a Post
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the post to update
        requestBody:
          required: true
          content:
            application/json:
              schema: schemas.PostUpdate
        responses:
          200:
            description: Post updated successfully
          404:
            description: Post not found
    """
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
