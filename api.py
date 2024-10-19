from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.score})"


user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("score", type=int, required=True, help="Score cannot be blank")

userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "score": fields.Integer,
}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.order_by(desc(UserModel.score)).all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], score=args["score"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.order_by(desc(UserModel.score)).all()
        if len(users) > 10:
            user_to_delete = users[-1]
            db.session.delete(user_to_delete)
            db.session.commit()

        users = UserModel.query.order_by(desc(UserModel.score)).all()
        return users, 201


api.add_resource(Users, "/api/users/")


@app.route("/")
def home():
    return "<h1>Flask REST API</h1>"


if __name__ == "__main__":
    app.run(debug=True)
