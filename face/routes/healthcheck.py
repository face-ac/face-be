import logging

from flask import Blueprint

from face.utils.responses import response_with
from face.utils import responses as resp

healthcheck_api = Blueprint("healthcheck_api", __name__)


@healthcheck_api.route("/healthcheck", methods=["GET"])
def healthcheck():
    try:
        return response_with(resp.SUCCESS_200, message="i'm alive")
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)
