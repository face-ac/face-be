#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

# noinspection PyUnresolvedReferences
import face.db.models.access

access_api = Blueprint("access_api", __name__)
