#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from face.db.config import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Face(db.Model):
    # noinspection SpellCheckingInspection
    __tablename__ = "face"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
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


class FaceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Face
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    fname = fields.String()
    lname = fields.String()
    created = fields.String(dump_only=True)
    updated = fields.String(dump_only=True)
