from tokenize import endpats

from flask import Flask, g
from flask_restful import Api
from controller import main, courseController, ChoiceCourseController, StSchedule
import env
from model.model import database

app = Flask ( __name__)
app.secret_key = env.secret_key
app.config['SECRET_KEY'] = env.secret_key
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

api = Api (app)
api.add_resource (main.Login, '/login', endpoint= 'login')
api.add_resource (courseController.List, '/courses', endpoint= 'courses')
api.add_resource (ChoiceCourseController.List,'/choice_course_list',endpoint='choice_course_list')
api.add_resource (ChoiceCourseController.Store,'/choice_course',endpoint='add_choice_course')
api.add_resource (ChoiceCourseController.Delete,'/choice_course',endpoint='delete_choice_course')
api.add_resource (StSchedule.List,'/StSchedule',endpoint='StSchedule')

if __name__ == '__main__':
    database.connect ()
    app.run ('127.0.0.1', 5000)
