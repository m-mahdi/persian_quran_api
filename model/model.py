#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from  peewee import *
from peewee import SqliteDatabase, Model, IntegerField, DateTimeField, CharField, PrimaryKeyField, MySQLDatabase, SQL, \
    Field
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import env

# from model.Enum import EnumField

__author__ = 'mahdi'
database = MySQLDatabase('qurandb', user='root', password='',
                         host='127.0.0.1', port=3306)


class BaseModel(Model):
    class Meta:
        database = database

# ------------EnumField--------------
class EnumField(Field):
    db_field = "enum"

    def pre_field_create(self, model):
        field = "e_%s" % self.name

        self.get_database().get_conn().cursor().execute(
            "DROP TYPE IF EXISTS %s;" % field
        )

        query = self.get_database().get_conn().cursor()

        tail = ', '.join(["'%s'"] * len(self.choices)) % tuple(self.choices)
        q = "CREATE TYPE %s AS ENUM (%s);" % (field, tail)
        query.execute(q)

    def post_field_create(self, model):
        self.db_field = "e_%s" % self.name

    def coerce(self, value):
        if value not in self.choices:
            raise Exception("Invalid Enum Value `%s`", value)
        return str(value)

    def get_column_type(self):
        return "enum"

    def __ddl_column__(self, ctype):
        return SQL("e_%s" % self.name)
# --------------end EnumField-----------------------------

# -----------course-----------------
class course(BaseModel):
    id = PrimaryKeyField()
    presentation = EnumField(choices=["theoretic", "practical"])
    type = EnumField(choices=["basic", "prime", "professional", "public"])
    name = CharField()
    unit_number = IntegerField()
    price = CharField()
    status_prerequisite = EnumField(choices=["yes", "no"])
    list_prerequisite = CharField()

    class Meta:
        db_table = "course"

# -----------------group_course-----------------
class group_course(BaseModel):
    code_course = PrimaryKeyField()
    group_number = CharField()
    semester = CharField()
    capacity = IntegerField()
    min_capacity = IntegerField()
    Course_id = IntegerField()
    professor_id = IntegerField()
    Time_Course_id = IntegerField()
    guest_semester = CharField()
    date_exam = CharField()
    time_exam = CharField()
    term = CharField()

    class Meta:
        db_table = "group_course"

# -----------------professor------------------
class professor(BaseModel):

    id = PrimaryKeyField()
    firstname = CharField()
    lastname = CharField()
    father = CharField()
    sex = EnumField(choices=["male","female"])
    national_code = CharField()
    birthday = CharField()
    location_brith = CharField()
    password = TextField()
    phone = CharField()
    mobile = CharField()
    address = TextField()
    img = CharField()

    class Meta:
        db_table = "professor"

# -----------------Choice_Course-----------------
# class Choice_Course(BaseModel):
#     id = PrimaryKeyField()
#     Student_student_number = ForeignKeyField(Student)
#     status = EnumField(choices=["accept", "non_accept"])
#     score = FloatField()
#     semeter = CharField()
#     Group_Course_code_course = ForeignKeyField(group_course)
#     status_pay = EnumField(choices=["yes", "on"])
#
#     class Meta:
#         db_table = "choice_course"



# ------------Time_Course--------------
class Time_Course(BaseModel):
    id = PrimaryKeyField()
    days = IntegerField()
    time = IntegerField()
    classes = IntegerField()
    rotatory = EnumField(choices=['1', '2'])
    day_rotatory = EnumField(choices=['zoj', 'fard'])

    class Meta:
        db_table = "time_course"


# -------------------Student------------------------
class Student(BaseModel):
    firstname = CharField()
    lastname = CharField()
    father = CharField()
    brithday = CharField()
    location_brith = CharField()
    phone = CharField()
    mobile = CharField()
    national_code = CharField()
    status = EnumField(choices=['active', 'non_active', 'expulsion', 'alumnus'])
    entry_semester = CharField()
    address = TextField()
    student_number = PrimaryKeyField()
    id = CharField()
    password = CharField()
    img = CharField()

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(env.secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(env.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        try:
            user = Student.get(Student.id == data['id'])
            return user
        except:
            return None

    class Meta:
        db_table = "student"
        order_by = ('student_number',)


    #
    # if __name__ == '__main__':
    #
    # a.id = student()
    # a.username = "ali"
    # u.hash_password("123")
    # u.enabled = 1
    # u.save()
    #
    # u = student()
    # u.username = "hassan"
    # u.hash_password("123456")
    # u.enabled = 1
    # u.save()
