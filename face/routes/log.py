#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint
from flask import request
from face.utils.responses import response_with
from face.utils import responses as resp

log_api = Blueprint("log_api", __name__)


@log_api.route("/log", methods=["POST"])
def log():
    try:
        data = request.get_json()
        print(data)

        return response_with(resp.SUCCESS_200, value={"status": "logged"})
    except Exception as e:
        logging.error(e)
        return response_with(resp.INVALID_INPUT_422)
