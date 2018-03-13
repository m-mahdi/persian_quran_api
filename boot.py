
from flask import Flask, g
from flask_restful import Api
from controller import main,courseController
import env
from model.model import database

app = Flask ( __name__)
app.secret_key = env.secret_key
app.config['SECRET_KEY'] = env.secret_key
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

api = Api (app)

api.add_resource (main.Login, '/login', endpoint= 'login')
api.add_resource (courseController.List, '/courses', endpoint= 'courses')
api.add_resource (main.Main, '/', endpoint= 'index')

if __name__ == '__main__':
    database.connect ()
    app.run ('0.0.0.0', 5000, True)
