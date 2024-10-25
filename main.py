from datetime import datetime
from http.client import HTTPException
from flask import Flask, request, abort, jsonify
from random import randrange
from http import HTTPStatus

app = Flask(__name__)

from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    timestamp: datetime = datetime.now()

all_posts = [
    {
        "id": 1,
        "title": "Discover the Serenity of Malpe Beach",
        "content": "Explore Malpe Beach, known for its pristine sands and tranquil waters. Perfect for a relaxing summer getaway!"
    },
    {
        "id": 2,
        "title": "Adventurous Times at Gokarna Beach",
        "content": "Get ready for adventure at Gokarna Beach! Enjoy water sports, beach trekking, and stunning sunset views."
    },
    {
        "id": 3,
        "title": "Unwind at Kudle Beach",
        "content": "Kudle Beach offers a laid-back vibe with beautiful surroundings. Ideal for sunbathing and enjoying a peaceful day by the sea."
    },
    {
        "id": 4,
        "title": "Experience the Charm of Om Beach",
        "content": "Visit Om Beach, famous for its unique shape and spiritual significance. A must-see for beach lovers and soul seekers!"
    },
    {
        "id": 5,
        "title": "Fun in the Sun at Paradise Beach",
        "content": "Paradise Beach is a hidden gem! Enjoy soft sands, clear waters, and a chance to escape the crowds for a perfect summer day."
    }
]

@app.route("/")
def hello_world():
    return {"message": "Hello, World!!!"}

@app.route("/posts", methods = ['GET', 'POST'])
def get_and_create_posts():
    if request.method == 'POST':
        try:
            # Parse and validate the JSON body using Pydantic
            post_data = Post(**request.get_json())
            post = post_data.dict()
            post['id'] = randrange(0,100000)
            all_posts.append((post))
            return {"message": "successfully created a single post", "data": post_data.dict()}, HTTPStatus.CREATED
        except Exception as e:
            abort(HTTPStatus.BAD_REQUEST)
    else:
        return all_posts

@app.route("/posts/<int:id>", methods=['GET'])
def read_post(id):
    post = next((post for post in all_posts if post['id'] == id), None)
    if post is None:
        return {"message": f"post with id:{id} was not found"}
        abort(HTTPStatus.NOT_FOUND)  # Not found
    # return jsonify(post)
    return post

@app.route("/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    for i, post in enumerate(all_posts):
        if post['id'] == id:
            print(i)
            print(post)
            all_posts.pop(i)
            return {"message": f"post with id:{id} was deleted"}
    return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND


@app.route("/posts/<int:id>", methods=['PUT'])
def updatePost(id):
    post_data = Post(**request.get_json())
    updated_post = post_data.dict()
    updated_post['id']=id
    for i, post in enumerate(all_posts):
        if post['id'] == id:
            all_posts[i] = updated_post
            return all_posts
    return {"message": f"post with id:{id} was not found"}, HTTPStatus.NOT_FOUND

