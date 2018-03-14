#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


from passlib.handlers.bcrypt import bcrypt
from peewee import *
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
class Course(BaseModel):
    id = PrimaryKeyField()
    presentation = EnumField(choices=["theoretic", "practical"])
    type = EnumField(choices=["basic", "prime", "professional", "public"])
    name = CharField(45)
    unit_number = IntegerField(11)
    price = CharField(45)
    status_prerequisite = EnumField(choices=["yes", "no"])
    list_prerequisite = CharField(255)

    class Meta:
        db_table = "course"


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
        self.password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

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

    def hash_password(self, password):
        # self.password = pwd_context.encrypt(password)
        self.password = pwd_context.bcrypt(password)
        self.password = bcrypt.hash(password)
    #
    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password)
    #
    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(env.secret_key, expires_in=expiration)
    #     return s.dumps({'id': self.id})
    #
    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(env.secret_key)
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None  # valid token, but expired
    #     except BadSignature:
    #         return None  # invalid token
    #     try:
    #         user = Student.get(Student.id == data['id'])
    #         return user
    #     except:
    #         return None
    #
    class Meta:
        db_table = "student"
        order_by = ('student_number',)

# -----------------professor------------------
class Professor(BaseModel):

    id = PrimaryKeyField()
    firstname = CharField(45)
    lastname = CharField(45)
    father = CharField(45)
    sex = EnumField(choices=["male","female"])
    national_code = CharField(45)
    birthday = CharField(45)
    location_brith = CharField(45)
    password = TextField()
    phone = CharField(45)
    mobile = CharField(45)
    address = TextField()
    img = CharField(255)

    class Meta:
        db_table = "professor"


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


# -----------------group_course-----------------
class group_Course(BaseModel):
    code_course = PrimaryKeyField()
    group_number = CharField(45)
    semester = CharField(45)
    capacity = IntegerField(11)
    min_capacity = IntegerField(11)
    Course_id = ForeignKeyField(Course)
    professor_id = professor_id = ForeignKeyField(Professor, backref='group_course')
    Time_Course_id = ForeignKeyField(Time_Course)
    guest_semester = CharField(255)
    date_exam = CharField(45)
    time_exam = CharField(45)
    term = CharField(45)

    class Meta:
        db_table = "group_course"

# -----------------Choice_Course-----------------
class Choice_Course(BaseModel):
    id = PrimaryKeyField()
    Student_student_number = ForeignKeyField(Student, field='id')
    status = EnumField(choices=["accept", "non_accept"])
    score = FloatField()
    semeter = CharField()
    Group_Course_code_course = ForeignKeyField(group_Course, field='id')
    status_pay = EnumField(choices=["yes", "on"])

    class Meta:
        db_table = "choice_course"
        indexes = (('Student_student_number', 'Group_Course_code_course'), True)

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
