#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint
from flask import request
from sqlalchemy.exc import IntegrityError
from face.db.models.access_point import AccessPointSchema, AccessPoint
from face.utils.auth import authenticate_jwt
from face.utils.constants import notFound, permission, required, exists, invalid
from face.utils.responses import response_with
from face.utils import responses as resp

access_point_api = Blueprint("access_point_api", __name__)


@access_point_api.route("/access_point", methods=["POST"])
@authenticate_jwt
def create_access_point():
    try:
        data = request.get_json()
        access_point_schema = AccessPointSchema()
        ap, error = access_point_schema.load(data)
        result = access_point_schema.dump(ap.create()).data
        return response_with(resp.SUCCESS_200, value={"accessPoint": result})
    except Exception as e:
        logging.error(e)
        return response_with(resp.INVALID_INPUT_422)


@access_point_api.route("/access_point/<aid>", methods=["GET"])
@authenticate_jwt
def get_access_point_details(aid):
    try:
        ap = AccessPoint.query.filter_by(id=aid).first()
        if not ap:
            error = notFound.format("Access Point")
            return response_with(resp.NOT_FOUND_HANDLER_404, error=error)

        access_point_schema = AccessPointSchema()
        ap_data, error = access_point_schema.dump(ap)
        if error:
            return response_with(resp.SERVER_ERROR_500, error=error)

        val = {
            "id": ap_data["id"],
            "name": ap_data["name"],
            "created": ap_data["created"],
            "updated": ap_data["updated"],
        }

        return response_with(resp.SUCCESS_200, value={"accessPoint": val})
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@access_point_api.route("/access_point/<aid>", methods=["PUT"])
@authenticate_jwt
def update_access_point(aid):
    try:
        data = request.get_json()

        name = data.get("name")
        if not name:
            e = required.format("Name")
            return response_with(resp.MISSING_PARAMETERS_422, error=e)

        # validate access point exists
        ap = AccessPoint.query.filter_by(id=aid).first()
        if not ap:
            e = notFound.format("Access Point")
            return response_with(resp.NOT_FOUND_HANDLER_404, error=e)

        # update access point
        ap.update(name)

        # response details
        return response_with(resp.SUCCESS_200)
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)
