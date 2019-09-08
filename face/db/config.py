#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", 3306)
    DB_SCHEMA = os.environ.get("DB_SCHEMA", "face_be")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        Config.DB_USER, Config.DB_PASSWORD, Config.DB_HOST, Config.DB_SCHEMA
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        Config.DB_USER, Config.DB_PASSWORD, Config.DB_HOST, Config.DB_SCHEMA
    )
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    circle = os.environ.get("CIRCLE", "no")
    if circle == "yes":
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}@{}/{}".format(
            Config.DB_USER, Config.DB_HOST, Config.DB_SCHEMA
        )
    else:
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
            Config.DB_USER, Config.DB_PASSWORD, Config.DB_HOST, Config.DB_SCHEMA
        )
    SQLALCHEMY_ECHO = False
