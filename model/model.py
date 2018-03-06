#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from peewee import SqliteDatabase, Model, IntegerField, DateTimeField, CharField, PrimaryKeyField, MySQLDatabase, SQL, \
    Field
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import env

# from model.Enum import EnumField

__author__ = 'Zaaferani'
database = MySQLDatabase('qurandb', user='root', password='',
                         host='127.0.0.1', port=3306)


class BaseModel(Model):
    class Meta:
        database = database


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


# noinspection PyBroadException
# class Users(BaseModel):
#     id = PrimaryKeyField()
#     username = CharField(unique=True)
#     password = CharField()
#     enabled = IntegerField(default=1)
#
#     def hash_password(self, password):
#         self.password = pwd_context.encrypt(password)
#
#     def verify_password(self, password):
#         return pwd_context.verify(password, self.password)
#
#     def generate_auth_token(self, expiration=600):
#         s = Serializer(env.secret_key, expires_in=expiration)
#         return s.dumps({'id': self.id})
#
#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(env.secret_key)
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None  # valid token, but expired
#         except BadSignature:
#             return None  # invalid token
#         try:
#             user = Users.get(Users.id == data['id'])
#             return user
#         except:
#             return None
#
#     class Meta:
#         db_table = "users"
#         order_by = ('id',)


# class Books(BaseModel):
#     id = PrimaryKeyField()
#     title = CharField(50)
#     author = CharField(30)
#
#     class Meta:
#         db_table = "books"

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



    # if __name__ == '__main__':

    # u = Users()
    # u.username = "ali"
    # u.hash_password("123")
    # u.enabled = 1
    # u.save()
    #
    # u = Users()
    # u.username = "hassan"
    # u.hash_password("123456")
    # u.enabled = 1
    # u.save()
