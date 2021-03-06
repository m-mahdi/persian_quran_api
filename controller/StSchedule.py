__author__ = 'mahdi'

from flask_restful import Resource
from main import auth2
from model.model import group_Course


class List(Resource):
    @auth2.login_required
    def get(self):
        group_courses = group_Course.select()
        ls = [
            dict(
                id=group_course.id,
                group_number=group_course.group_number,
                term=group_course.term,
                Course_id=dict(
                    id=group_course.Course_id.id,
                    presentation=group_course.Course_id.presentation,
                    type=group_course.Course_id.type,
                    name=group_course.Course_id.name,
                    unit_number=group_course.Course_id.unit_number,
                    price=group_course.Course_id.price,
                    status_prerequisite=group_course.Course_id.status_prerequisite,
                    list_prerequisite=group_course.Course_id.list_prerequisite,
                ),
                professor_id=dict(
                    firstname=group_course.professor_id.firstname,
                    lastname=group_course.professor_id.lastname,

                ),
                Time_Course_id=dict(
                    id =group_course.Time_Course_id.id,
                    days =group_course.Time_Course_id.days,
                    time =group_course.Time_Course_id.time,
                    classes =group_course.Time_Course_id.classes,
                    rotatory = group_course.Time_Course_id.rotatory,
                    day_rotatory=group_course.Time_Course_id.day_rotatory,
                ),
        ) for group_course in group_courses
        ]
        return dict( stschedule=ls )

