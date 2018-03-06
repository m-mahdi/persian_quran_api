
from flask import Flask, g
from flask_restful import Api
from controller import courseController
import env
from model.model import database, course

app = Flask(__name__)
app.secret_key = env.secret_key
app.config['SECRET_KEY'] = env.secret_key

api = Api(app)

api.add_resource(courseController.List, '/courses', endpoint='c')
# api.add_resource(main.Main, '/', endpoint='index')

if __name__ == '__main__':
    database.connect()

    # database.create_tables([Users, course,True])

    app.run('0.0.0.0', 5000)