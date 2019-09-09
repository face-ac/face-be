#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
from flask import Flask
from flask_cors import CORS
from face.db.config import db
from face.utils.exception import (
    AuthRequired,
    ExpiredSignatureError,
    DecodeError,
    BaseJWTError,
)
from face.utils.responses import response_with
import face.utils.responses as resp
from face.routes.user import user_api
from face.routes.healthcheck import healthcheck_api


def create_app(config):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config)

    app.register_blueprint(healthcheck_api, url_prefix="/api")
    app.register_blueprint(user_api, url_prefix="/api")

    # START GLOBAL HTTP CONFIGURATIONS
    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.NOT_FOUND_HANDLER_404)

    @app.errorhandler(AuthRequired)
    def auth_required(e):
        logging.error(e)
        return response_with(resp.UNAUTHORIZED_403, error=e.error)

    @app.errorhandler(DecodeError)
    def decode_error(e):
        logging.error(e)
        return response_with(resp.UNAUTHORIZED_403, error=e.error)

    @app.errorhandler(ExpiredSignatureError)
    def expired_error(e):
        logging.error(e)
        return response_with(resp.UNAUTHORIZED_403, error=e.error)

    @app.errorhandler(BaseJWTError)
    def base_jwt_error(e):
        logging.error(e)
        return response_with(resp.UNAUTHORIZED_403, error=e.error)

    # END GLOBAL HTTP CONFIGURATIONS

    db.init_app(app)
    with app.app_context():
        db.create_all()

    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s",
        level=logging.DEBUG,
    )
    return app
