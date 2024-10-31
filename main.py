from datetime import datetime
from flask import Flask, request, abort, jsonify
from random import randrange
from http import HTTPStatus
from pydantic import BaseModel
import psycopg2
# to get the column names with the row data
from psycopg2.extras import RealDictCursor
import time

from .database import app
from .models import db, Post

with app.app_context():
    db.create_all()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="flaskapi",
#             user="postgres",
#             password="Nagashree@postgres",
#             port=5432,
#             cursor_factory=RealDictCursor
#         )
#         cur = conn.cursor()
#         print("Database Connection was successfull")
#         break
#     except Exception as error:
#         print("Database Connection Failed")
#         print("Error:", error)
#         time.sleep(2)


#
# class Post(BaseModel):
#     id: int = randrange(0,10000)
#     title: str
#     content: str
#     published: bool = True
#     timestamp: datetime = datetime.now()

@app.route("/")
def hello_world():
    return {"message": "Hello, World!!!"}


@app.route("/posts", methods=['GET', 'POST'])
def get_and_create_posts():
    if request.method == 'POST':
        new_post = Post(**request.get_json())
        print(new_post)
        # # cur.execute(f""" INSERT INTO posts(id,title,content,published) VALUES({post_data.id}, {post_data.title}, {post_data.content},{post_data.published})""")
        # #above code can cause sql injection
        # cur.execute(""" INSERT INTO posts(id,title,content,published) VALUES(%s, %s, %s, %s) RETURNING *""",(post.id, post.title, post.content,post.published))
        # new_post = cur.fetchone()
        # conn.commit()
        # return {"cerated new post": new_post}, HTTPStatus.CREATED
        #
        db.session.add(new_post)
        db.session.commit()
        # db.session.refresh(new_post)
        print(new_post)
        return {"message": new_post.title}, HTTPStatus.CREATED
    else:
        # cur.execute("SELECT * FROM posts;")
        # posts = cur.fetchall()

        # users = db.session.execute(db.select(Post).order_by(User.username)).scalars()
        posts = Post.query.all()
        result = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published
            }
            result.append(post_data)
        return result, HTTPStatus.OK


@app.route("/posts/<int:id>", methods=['GET'])
def read_post(id):
    print(id)
    # cur.execute("""SELECT * FROM posts p where p.id= %s;""",(str(id),))
    # post = cur.fetchone()
    post = db.get_or_404(Post, id)
    if not post:
        return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND
    print(post)
    # return post
    return {"post": post.title}


@app.route("/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    print(id)
    # cur.execute("""DELETE FROM posts p where p.id = %s RETURNING *""", (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    if post:
        return {"deleted data": post.title}, HTTPStatus.NO_CONTENT
    return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND


@app.route("/posts/<int:id>", methods=['PUT'])
def update_post(id):
    post = Post(**request.get_json())
    cur.execute(""" UPDATE posts p SET title=%s, content=%s, published=%s WHERE p.id=%s RETURNING *""",
                (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)
