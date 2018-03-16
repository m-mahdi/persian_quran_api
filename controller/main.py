#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import session, url_for, request, redirect, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from model.model import Student
from flask_restful import Resource

__author__ = 'mahdi'

auth = HTTPBasicAuth()
auth2 = HTTPTokenAuth()


# # noinspection PyBroadException
# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = Student.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         try:
#             user = Student.get(Student.student_number == username_or_token)
#         except:
#             user = None
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True
#
#
# @auth2.verify_token
# def verify_token(token):
#     user = Student.verify_auth_token(token)
#     if user:
#         g.user = user
#         return True
#     return False

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Student.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        try:
            user = Student.get(Student.student_number == username_or_token)
        except:
            user = None
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth2.verify_token
def verify_token(token):
    user = Student.verify_auth_token(token)
    if user:
        g.user = user
        return True
    return False

class Login (Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}

    @auth.login_required
    def post(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}





class Main (Resource):
    @auth2.login_required
    def get(self):
        return dict(username=g.user.student_number, id=g.user.student_number)

    @auth2.login_required
    def post(self):
        return dict(username=g.user.student_number, id=g.user.student_number)

