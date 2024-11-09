from functools import wraps
from http import HTTPStatus

from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from app import schemas
from app.models import Vote, db, Post
from app.oauth2 import CredentialException, verify_access_token

votes_bp = Blueprint('votes_bp', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'error': 'Not authenticated', 'message': 'Token is missing !!'}), HTTPStatus.UNAUTHORIZED

        try:
            current_user = verify_access_token(token)
        except CredentialException as e:
            return jsonify({'error': 'Not authenticated', 'message': str(e)}), HTTPStatus.UNAUTHORIZED

        return f(current_user, *args, **kwargs)

    return decorated


@votes_bp.route("/", methods=['POST'])
@token_required
def vote(current_user):
    # in body, post_id and dir
    # get user_id from current user

    data = request.get_json()
    vote_data = schemas.Vote(**data)
    post_id = vote_data.post_id
    dir = vote_data.dir
    user_id = current_user.get('user_id')

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": f"The post with id {post_id} is not found"}), HTTPStatus.NOT_FOUND

    query = Vote.query.filter(and_(Vote.post_id == post_id, Vote.user_id == user_id))
    vote_found = query.first()
    if dir == 1:
        if vote_found:
            return jsonify({"error": f"User {user_id }has already voted for post {post_id}"}), HTTPStatus.CONFLICT
        try:
            new_vote_data = Vote(
                post_id=post_id,
                user_id=user_id
            )
            db.session.add(new_vote_data)
            db.session.commit()
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        if not vote_found:
            return jsonify({"error": "vote not found"}), HTTPStatus.NOT_FOUND
        try:
            db.session.delete(vote_found)
            db.session.commit()
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    no_of_votes = Vote.query.filter(Vote.post_id == post_id).count()
    # post.votes =
    print("---------")
    print(post.title)
    print(no_of_votes)
    post.votes = no_of_votes
    db.session.add(post)
    db.session.commit()

    return {"message": "successfully added the vote"}
