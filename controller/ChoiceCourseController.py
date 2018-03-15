__author__ = 'mahdi'
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import session, url_for, request, redirect, g
from pyramid.tests.test_predicates import predicate

from Model.model import Choice_Course, group_Course, Student, Course
from main import auth2


class List( Resource ):
    @auth2.login_required
    def get(self):
        choice_courses = Choice_Course.select().where( Choice_Course.Student_student_number == g.user.student_number )
        ls = [
            dict(
                id=Choice_Course.id,
                Student_student_number=Choice_Course,
                status=Choice_Course.status,
                score=Choice_Course.score,
                semeter=Choice_Course.semeter,
                status_pay=Choice_Course.status_pay,
                Group_Course_code_course=[dict(
                    code_course=Choice_Course.Group_Course_code_course.code_course,
                    group_number=Choice_Course.Group_Course_code_course.group_number,
                    semester=Choice_Course.Group_Course_code_course.semester,
                    guest_semester=Choice_Course.Group_Course_code_course.guest_semester,
                    date_exam=Choice_Course.Group_Course_code_course.date_exam,
                    time_exam=Choice_Course.Group_Course_code_course.time_exam,
                    term=Choice_Course.Group_Course_code_course.term,
                    capacity=Choice_Course.Group_Course_code_course.capacity,
                    min_capacity=Choice_Course.Group_Course_code_course.min_capacity,
                    Course_id=[dict(
                        id=Choice_Course.Group_Course_code_course.Course_id.id,
                        presentation=Choice_Course.Group_Course_code_course.Course_id.presentation,
                        type=Choice_Course.Group_Course_code_course.Course_id.type,
                        status_prerequisite=Choice_Course.Group_Course_code_course.Course_id.status_prerequisite,
                        name=Choice_Course.Group_Course_code_course.Course_id.name,
                        unit_number=Choice_Course.Group_Course_code_course.Course_id.unit_number,
                        price=Choice_Course.Group_Course_code_course.Course_id.price,
                        list_prerequisite=Choice_Course.Group_Course_code_course.Course_id.list_prerequisite,
                    )],
                    professor_id=[dict(
                        firstname=Choice_Course.Group_Course_code_course.professor_id.firstname,
                        lastname=Choice_Course.Group_Course_code_course.professor_id.lastname,

                    )],
                    Time_Course_id=[dict(
                        id=Choice_Course.Group_Course_code_course.Time_Course_id.id,
                        days=Choice_Course.Group_Course_code_course.Time_Course_id.days,
                        time=Choice_Course.Group_Course_code_course.Time_Course_id.time,
                        classes=Choice_Course.Group_Course_code_course.Time_Course_id.classes,
                        rotatory=Choice_Course.Group_Course_code_course.Time_Course_id.rotatory,
                        day_rotatory=Choice_Course.Group_Course_code_course.Time_Course_id.day_rotatory,
                    )]
                )],

            ) for Choice_Course in choice_courses
            ]
        return dict( courses=ls )


class Store( Resource ):
    @auth2.login_required
    def post(self):
        request_json = request.get_json( )
        choice_course = Choice_Course( )
        choice_course.Student_student_number = request_json['Student_student_number']
        choice_course.status = request_json['status']
        choice_course.status_pay = request_json['status_pay']
        choice_course.score = request_json['score']
        choice_course.semeter = request_json['semeter']
        choice_course.Group_Course_code_course = request_json['Group_Course_code_course']

        return dict(
            status=choice_course.save()
        )


class Delete(Resource):
    @auth2.login_required
    def delete(self):
        return dict(
            status=Choice_Course.delete().where(Choice_Course.Student_student_number == g.user.student_number).execute()
        )

