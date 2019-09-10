#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint
from flask import request
from sqlalchemy.exc import IntegrityError
from face.db.models.user import UserSchema, User
from face.utils.auth import authenticate_jwt, generate_jwt, JWT
from face.utils.constants import notFound, permission, required, exists, invalid
from face.utils.responses import response_with
from face.utils import responses as resp

user_api = Blueprint("user_api", __name__)


@user_api.route("/user", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user_schema = UserSchema()
        user, error = user_schema.load(data)
        result = user_schema.dump(user.create()).data
        return response_with(resp.SUCCESS_200, value={"user": result})
    except Exception as e:
        logging.error(e)
        return response_with(resp.INVALID_INPUT_422)


@user_api.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        fetched = User.query.filter_by(login=data["login"]).first()
        if not fetched:
            e = notFound.format("User")
            return response_with(resp.INVALID_INPUT_422, error=e)

        valid_password = User.validate_password(
            data["password"], fetched.password
        )
        if not valid_password:
            e = invalid.format("Password")
            return response_with(resp.INVALID_INPUT_422, error=e)

        user_schema = UserSchema()
        user, error = user_schema.dump(fetched)
        token = generate_jwt(user)
        return response_with(resp.SUCCESS_200, value={"user": user, "token": token})
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@user_api.route("/user/<uid>", methods=["GET"])
@authenticate_jwt
def get_user_details(uid):
    try:
        return _get_user(uid)
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@user_api.route("/user/<uid>", methods=["PUT"])
@authenticate_jwt
def update_user(uid):
    try:
        data = request.get_json()

        name = data.get("name")
        if not name:
            e = required.format("Name")
            return response_with(resp.MISSING_PARAMETERS_422, error=e)

        surname = data.get("surname")
        if not surname:
            e = required.format("Surname")
            return response_with(resp.MISSING_PARAMETERS_422, error=e)

        email = data.get("email")
        if not email:
            e = required.format("Email")
            return response_with(resp.MISSING_PARAMETERS_422, error=e)

        # validate user exists
        user = User.query.filter_by(id=uid).first()
        if not user:
            e = notFound.format("User")
            return response_with(resp.NOT_FOUND_HANDLER_404, error=e)

        # validate access to user
        access = User.query.filter_by(id=JWT.details["user_id"]).first()
        if not access:
            e = permission
            return response_with(resp.NOT_FOUND_HANDLER_404, error=e)

        # update user
        user.update(name, surname, email)

        # response details
        return _get_user(uid)
    except IntegrityError:
        e = exists.format("Name")
        return response_with(resp.INVALID_INPUT_422, error=e)
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@user_api.route("/validate", methods=["GET"])
@authenticate_jwt
def validate():
    try:
        uid = JWT.details["user_id"]
        return _get_user(uid)
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


def _get_user(uid):
    user = User.query.filter_by(id=uid).first()
    if not user:
        error = notFound.format("User")
        return response_with(resp.NOT_FOUND_HANDLER_404, error=error)

    user_schema = UserSchema()
    user_data, error = user_schema.dump(user)
    if error:
        return response_with(resp.SERVER_ERROR_500, error=error)

    val = {
        "id": user_data["id"],
        "firstName": user_data["name"],
        "lastName": user_data["surname"],
        "email": user_data["email"],
        "login": user_data["login"],
        "created": user_data["created"],
        "updated": user_data["updated"],
    }

    return response_with(resp.SUCCESS_200, value={"user": val})
