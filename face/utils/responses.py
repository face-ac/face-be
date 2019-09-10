#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "error": "Not all field names are valid",
}

INVALID_INPUT_422 = {"http_code": 422, "error": "Invalid input"}

MISSING_PARAMETERS_422 = {"http_code": 422, "error": "Missing parameters"}

BAD_REQUEST_400 = {"http_code": 400, "error": "Bad request"}

SERVER_ERROR_500 = {"http_code": 500, "error": "Server error"}

SERVER_ERROR_404 = {"http_code": 404, "error": "Resource not found"}

UNAUTHORIZED_403 = {"http_code": 403, "error": "You are not allowed to do that"}

NOT_FOUND_HANDLER_404 = {"http_code": 404, "error": "Handler not found"}

SUCCESS_200 = {"http_code": 200, "status": True}


def response_with(response, value=None, headers={}, error=None):
    result = {
        "status": response.get("status", False),
        "error": error if error is not None else response.get("error", None),
        "data": value if value is not None else {},
    }

    headers.update({"Access-Control-Allow-Origin": "*"})
    headers.update({"server": "face"})

    return make_response(jsonify(result), response["http_code"], headers)
