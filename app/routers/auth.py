
from http import HTTPStatus

from flask import Blueprint, request, jsonify

from app.models import db, User
from ..database import app
from ..utils import check_password
from app import schemas

auth_bp = Blueprint('auth_bp', __name__)
app.config['SECRET_KEY'] = 'your secret key'


@auth_bp.route("/login", methods=['POST'])
def login():
    try:
        login_data = schemas.Login(**request.get_json())
        print("Login data:", login_data)

        user_data = User.query.filter_by(email=login_data.email).first()
        if user_data is None:
            return jsonify({"message": "Invalid credentials"}), HTTPStatus.NOT_FOUND
        print("password in database", user_data.password)
        print("input password", login_data.password)

        if check_password(user_data.password, login_data.password):
            print("Password is correct")
            return jsonify({"message": "logged in"}), HTTPStatus.OK

        print("Password is incorrect")
        return jsonify({"message": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
