#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from face.db.config import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class AccessPoint(db.Model):
    # noinspection SpellCheckingInspection
    __tablename__ = "access_point"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise


class AccessPointSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AccessPoint
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String()
    created = fields.String(dump_only=True)
    updated = fields.String(dump_only=True)
