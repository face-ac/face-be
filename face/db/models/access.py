#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from face.db.config import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from face.db.models.user import User


class Access(db.Model):
    __tablename__ = "access"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user = db.Column(db.BigInteger, db.ForeignKey(User.id))
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime)

    def __init__(self, user):
        self.user = user

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise


class AccessSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Access
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    user = fields.Integer()
    created = fields.String(dump_only=True)
    updated = fields.String(dump_only=True)
