from flasgger import Swagger

from .database import app
from .models import db

from .routers.auth import auth_bp
from .routers.post import posts_bp
from .routers.user import users_bp

with app.app_context():
    db.create_all()

swagger = Swagger(app, template={
    "info": {
        "title": "My Flask API",
        "description": "An example API using Flask and Swagger",
        "version": "1.0.0"
    }
})


@app.route("/")
def hello_world():
    return {"message": "Hello, World!!!"}


app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(auth_bp, url_prefix='/auth')
