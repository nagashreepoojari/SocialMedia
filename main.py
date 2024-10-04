from flask import Flask, request

app = Flask(__name__)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()

@app.route("/")
def hello_world():
    return {"message": "Hello, World!!!"}

@app.route("/posts")
def hello_motto():
    return {"message": "lists of posts"}

@app.post("/createpost")
def createpost():
    data = request.get_json() 
    print(data)
    return data