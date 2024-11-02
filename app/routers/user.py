from http import HTTPStatus
from http.client import HTTPException
from random import randrange

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app import schemas
from app.models import db, User
from app.utils import hash_password

users_bp = Blueprint('users_bp', __name__)


@users_bp.route("/", methods=['GET'])
def get_all_users():
    """
        Get All Users
        ---
        responses:
          200:
            description: A list of all users
          500:
            description: Database error occurred
    """
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


@users_bp.route("/", methods=['POST'])
def create_user():
    """
        Create a New User
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema: schemas.UserCreate
        responses:
          201:
            description: User created successfully
          500:
            description: Database error occurred
    """
    try:
        data = request.get_json()
        user_data = schemas.UserCreate(**data)

        # Hash the password before storing it
        hashed_password = hash_password(user_data.password)

        new_user = User(
            id=randrange(0, 100000),
            email=user_data.email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(schemas.UserResponse.from_orm(new_user).dict()), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}),


@users_bp.route("/<int:id>", methods=['GET'])
def read_user(id):
    """
        Get a Single User
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the user to retrieve
        responses:
          200:
            description: User found
          404:
            description: User not found
    """
    try:
        user_data = User.query.get(id)
        if user_data is None:
            return jsonify({"message": f"User with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        user = schemas.UserResponse.from_orm(user_data).dict()
        return jsonify(user), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@users_bp.route("/<int:id>", methods=['DELETE'])
def delete_user(id):
    """
        Delete a User
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the user to delete
        responses:
          204:
            description: User deleted
          404:
            description: User not found
    """
    try:
        user = User.query.get(id)
        if user is None:
            return jsonify({"message": f"User with id:{id} was not found"}), HTTPStatus.NOT_FOUND
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User with id:{id} was deleted"}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@users_bp.route("/<int:id>", methods=['PUT'])
def update_user(id):
    """
        Update a User
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the user to update
        requestBody:
          required: true
          content:
            application/json:
              schema: schemas.UserUpdate
        responses:
          200:
            description: User updated successfully
          404:
            description: User not found
    """
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
