__author__ = 'mahdi'
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import session, url_for, request, redirect, g
from pyramid.tests.test_predicates import predicate

from model.model import Choice_Course, group_Course, Student, Course
from main import auth2


class List( Resource ):
    @auth2.login_required
    def get(self):
        choice_courses = Choice_Course.select().where( Choice_Course.Student_student_number == g.user.student_number )
        ls = [
            dict(
                id=choice_course.id,
                Student_student_number=choice_course,
                status=choice_course.status,
                score=choice_course.score,
                semeter=choice_course.semeter,
                status_pay=choice_course.status_pay,
                Group_Course_code_course=[dict(
                    code_course=choice_course.Group_Course_code_course.code_course,
                    group_number=choice_course.Group_Course_code_course.group_number,
                    semester=choice_course.Group_Course_code_course.semester,
                    guest_semester=choice_course.Group_Course_code_course.guest_semester,
                    date_exam=choice_course.Group_Course_code_course.date_exam,
                    time_exam=choice_course.Group_Course_code_course.time_exam,
                    term=choice_course.Group_Course_code_course.term,
                    capacity=choice_course.Group_Course_code_course.capacity,
                    min_capacity=choice_course.Group_Course_code_course.min_capacity,
                    Course_id=[dict(
                        id=choice_course.Group_Course_code_course.Course_id.id,
                        presentation=choice_course.Group_Course_code_course.Course_id.presentation,
                        type=choice_course.Group_Course_code_course.Course_id.type,
                        status_prerequisite=choice_course.Group_Course_code_course.Course_id.status_prerequisite,
                        name=choice_course.Group_Course_code_course.Course_id.name,
                        unit_number=choice_course.Group_Course_code_course.Course_id.unit_number,
                        price=choice_course.Group_Course_code_course.Course_id.price,
                        list_prerequisite=choice_course.Group_Course_code_course.Course_id.list_prerequisite,
                    )],
                    professor_id=[dict(
                        firstname=choice_course.Group_Course_code_course.professor_id.firstname,
                        lastname=choice_course.Group_Course_code_course.professor_id.lastname,

                    )],
                    Time_Course_id=[dict(
                        id=choice_course.Group_Course_code_course.Time_Course_id.id,
                        days=choice_course.Group_Course_code_course.Time_Course_id.days,
                        time=choice_course.Group_Course_code_course.Time_Course_id.time,
                        classes=choice_course.Group_Course_code_course.Time_Course_id.classes,
                        rotatory=choice_course.Group_Course_code_course.Time_Course_id.rotatory,
                        day_rotatory=choice_course.Group_Course_code_course.Time_Course_id.day_rotatory,
                    )]
                )],

            ) for choice_course in choice_courses
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

