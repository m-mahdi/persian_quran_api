from flask_restful import Resource

from main import auth2
from model.model import Course, group_Course

# -----------------careate model groupcourse---------------
class List(Resource):
    @auth2.login_required
    def get(self):
        group_courses = group_Course.select()
        ls = [
            dict(
                id=group_course.id,
                group_number=group_course.group_number,
                semester=group_course.semester,
                guest_semester=group_course.guest_semester,
                date_exam=group_course.date_exam,
                time_exam=group_course.time_exam,
                term=group_course.term,
                capacity=group_course.capacity,
                min_capacity=group_course.min_capacity,
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

        ) for group_course in group_courses
        ]
        return dict( courses=ls )

