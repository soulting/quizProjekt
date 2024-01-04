from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import psycopg2

app = Flask(__name__)
CORS(app)
api = Api(app)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwerty@localhost:5432/project"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    quiz_ids = Column(ARRAY(Integer))
    is_admin = Column(Boolean, nullable=False)
    icon_name = Column(String)


class Quizzes(db.Model):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    icon = Column(String)
    color = Column(String)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    option_a = db.Column(db.String)
    option_b = db.Column(db.String)
    option_c = db.Column(db.String)
    option_d = db.Column(db.String)
    answer = db.Column(db.String, nullable=False)
    explanation = db.Column(db.String)


class CreateUser(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"message": "ta nazwa użytkownika jest już zajęta "}, 409

        new_user = User(
            username=username,
            password=password,
            quiz_ids=[],
            is_admin=False,
            icon_name="default"

        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating user", "error": str(e)}, 500


class GetUser(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        try:
            existing_user = User.query.filter_by(username=username, password=password).first()
            if existing_user:
                responseData = {
                    "id": existing_user.id,
                    "username": existing_user.username,
                    "quiz_ids": existing_user.quiz_ids,
                    "is_admin": existing_user.is_admin,
                    "icon_name": existing_user.icon_name
                }
                print(responseData)
                return responseData, 200

            else:
                return {"message": "Invalid username or password"}, 401

        except Exception as e:
            db.session.rollback()
            return {"message": "Error finding user", "error": str(e)}, 500


class GetQuizHeaders(Resource):
    def post(self):
        data = request.json
        id_list = data.get('quiz_ids')

        lista_pytan = []

        try:
            for i in range(0, len(id_list)):
                quiz_header = Quizzes.query.filter_by(id=id_list[i]).first()
                if quiz_header:
                    quizData = {
                        "id": quiz_header.id,
                        "title": quiz_header.title,
                        "description": quiz_header.description,
                        "icon": quiz_header.icon,
                        "color": quiz_header.color
                    }
                    lista_pytan.append(quizData)
            resposeData = {
                "quiz_headers": lista_pytan
            }

            return resposeData, 200


        except Exception as e:
            db.session.rollback()
            return {"message": "Error finding user", "error": str(e)}, 500


class SearchQuizzes(Resource):
    def post(self):
        data = request.json
        frase = data.get('frase')

        lista_quizow = []

        try:
            quizzes = Quizzes.query.all()
            if quizzes:
                for quiz in quizzes:
                    if frase in quiz.title:
                        data = {
                            "id": quiz.id,
                            "title": quiz.title,
                            "description": quiz.description,
                            "icon": quiz.icon
                        }
                        lista_quizow.append(data)
                resposeData = {
                    "quizzes": lista_quizow
                }

                return resposeData, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Error finding user", "error": str(e)}, 500


class GetQuestions(Resource):
    def post(self):
        data = request.json
        id = data.get('id')
        lista_pytan = []

        try:
            questions = Question.query.filter_by(quiz_id=id).all()
            if questions:
                for question in questions:
                    data = {
                        "id": question.id,
                        "question": question.question,
                        "option_A": question.option_a,
                        "option_B": question.option_b,
                        "option_C": question.option_c,
                        "option_D": question.option_d,
                        "answer": question.answer,
                        "explanation": question.explanation
                    }
                    lista_pytan.append(data)

                    # print(data)

                responseData = {
                    "questions": lista_pytan
                }

                return responseData, 200

            return {"message": "No questions found for the given quiz ID"}, 404

        except Exception as e:
            db.session.rollback()
            return {"message": "Error finding questions", "error": str(e)}, 500


class AddQuiz(Resource):
    def post(self):
        data = request.json
        userId = data.get('userId')
        quizId = data.get('quizId')
        keyInput = data.get('keyInput')

        if keyInput != "hasło":
            returnData = {
                "accepted": False,
            }
            return returnData, 200

        try:
            user = User.query.filter_by(id=userId).first()
            if user:
                new_quiz_list = [int(quizId)]
                new_quiz_list += user.quiz_ids
                user.quiz_ids = list(set(new_quiz_list))
                db.session.commit()

                returnData = {
                    "accepted": True,
                    "new_quiz_list": user.quiz_ids
                }

                return returnData, 200

            return {"message": "No questions found for the given quiz ID"}, 404

        except Exception as e:
            db.session.rollback()
            return {"message": "Error finding questions", "error": str(e)}, 500


class DeleteQuiz(Resource):
    def post(self):
        data = request.json
        userId = data.get('userId')
        quizId = data.get('quizId')

        try:
            user = User.query.filter_by(id=userId).first()
            if user:
                new_quiz_list = []
                for i in user.quiz_ids:
                    if i != int(quizId):
                        new_quiz_list.append(i)

                user.quiz_ids = new_quiz_list
                db.session.commit()

                returnData = {
                    "new_quiz_list": user.quiz_ids
                }

                return returnData, 200

            return {"message": "No questions found for the given quiz ID"}, 404

        except Exception as e:
            db.session.rollback()
            return {"message": "Error finding questions", "error": str(e)}, 500


api.add_resource(CreateUser, '/sign-in')
api.add_resource(GetUser, '/login')
api.add_resource(GetQuizHeaders, '/loadQuizHeaders')
api.add_resource(SearchQuizzes, '/searchQuizzes')
api.add_resource(GetQuestions, '/getQuestions')
api.add_resource(AddQuiz, '/addQuiz')
api.add_resource(DeleteQuiz, '/deleteQuiz')

if __name__ == '__main__':
    app.run(debug=True)
