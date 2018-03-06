from flask.ext.restful import Resource

from  model.model import course


class List(Resource):
    def get(self):
        courses = course.select()
        ls = [
            dict(
                id=c.id,
                presentation=c.presentation,
                type=c.type,
                name=c.name,
                unit_number=c.unit_number,
                price=c.price,
                status_prerequisite=c.status_prerequisite,
                list_prerequisite=c.list_prerequisite,
            ) for c in courses
            ]
        return dict(courses=ls)
