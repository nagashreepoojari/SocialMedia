from flasgger import Swagger
from datetime import datetime
from flask import Flask, request, abort, jsonify
from random import randrange
from http import HTTPStatus
from pydantic import BaseModel
import psycopg2
# to get the column names with the row data
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="flaskapi",
            user="postgres",
            password="Nagashree@postgres",
            port=5432,
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        print("Database Connection was successfull")
        break
    except Exception as error:
        print("Database Connection Failed")
        print("Error:", error)
        time.sleep(2)

app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "My Flask API",
        "description": "An example API using Flask and Swagger",
        "version": "1.0.0"
    }
})


class Post(BaseModel):
    id: int = randrange(0,10000)
    title: str
    content: str
    published: bool = True
    timestamp: datetime = datetime.now()

@app.route("/")
def hello_world():
    """
    Hello World
    ---
    responses:
      200:
        description: Returns a greeting message
    """
    return {"message": "Hello, World!!!"}


@app.route("/posts", methods=['GET', 'POST'])
def get_and_create_posts():
    """
    Create or Get Posts
    ---
    get:
      description: Get all posts
      responses:
        200:
          description: List of all posts
    post:
      description: Create a new post
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                content:
                  type: string
      responses:
        201:
          description: Post created successfully
    """
    if request.method == 'POST':
        post = Post(**request.get_json())
        print(post)
        # cur.execute(f""" INSERT INTO posts(id,title,content,published) VALUES({post_data.id}, {post_data.title}, {post_data.content},{post_data.published})""")
        #above code can cause sql injection
        cur.execute(""" INSERT INTO posts(id,title,content,published) VALUES(%s, %s, %s, %s) RETURNING *""",(post.id, post.title, post.content,post.published))
        new_post = cur.fetchone()
        conn.commit()
        return {"cerated new post": new_post}, HTTPStatus.CREATED
        # try:
        #     post_data = Post(**request.get_json())
        #     post = post_data.dict()
        #     post['id'] = randrange(0, 100000)
        #     all_posts.append(post)
        #     return {"message": "successfully created a single post", "data": post_data.dict()}, HTTPStatus.CREATED
        # except Exception as e:
        #     abort(HTTPStatus.BAD_REQUEST)
    else:
        cur.execute("SELECT * FROM posts;")
        posts = cur.fetchall()
        print(posts)
        return posts, HTTPStatus.OK


@app.route("/posts/<int:id>", methods=['GET'])
def read_post(id):
    """
    Get a Post
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The post ID
    responses:
      200:
        description: The post data
      404:
        description: Post not found
    """
    print(id)
    cur.execute("""SELECT * FROM posts p where p.id= %s;""",(str(id),))
    post = cur.fetchone()
    if not post:
        return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND
    print(post)
    return post


@app.route("/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    """
    Delete a Post
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The post ID
    responses:
      204:
        description: Post deleted
      404:
        description: Post not found
    """
    print(id)
    cur.execute("""DELETE FROM posts p where p.id = %s RETURNING *""", (str(id),))
    deleted_post = cur.fetchone()
    print(deleted_post)
    conn.commit()
    if deleted_post:
        return {"deleted data": deleted_post}, HTTPStatus.NO_CONTENT
    return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND




@app.route("/posts/<int:id>", methods=['PUT'])
def update_post(id):
    """
    Update a Post
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The post ID
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              content:
                type: string
    responses:
      200:
        description: Post updated
      404:
        description: Post not found
    """
    post = Post(**request.get_json())

    cur.execute(""" UPDATE posts p SET title=%s, content=%s, published=%s WHERE p.id=%s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND
