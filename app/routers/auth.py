from http import HTTPStatus

from flask import Blueprint, request, jsonify

from app.models import db, User
from ..database import app
from ..utils import check_password
from app import schemas
from ..oauth2 import create_access_token
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

        if not check_password(user_data.password, login_data.password):
            print("Password is incorrect")
            return jsonify({"message": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED

        # create jwt token and send back
        access_token = create_access_token(data={"user_id": user_data.id})
        return jsonify({"access_token": access_token, "token_type": "bearer"}), HTTPStatus.OK

    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
