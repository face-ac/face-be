#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from face.db.config import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class AccessRecord(db.Model):
    # noinspection SpellCheckingInspection
    __tablename__ = "access_record"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    status = db.Column(db.String(255), nullable=False)
    access_time = db.Column(db.DateTime, nullable=False)
    # face FK
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime)

    def __init__(self, status, access_time):
        self.status = status
        self.access_time = access_time

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise


class AccessRecordSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AccessRecord
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    status = fields.String()
    access_time = fields.String()
    created = fields.String(dump_only=True)
    updated = fields.String(dump_only=True)
