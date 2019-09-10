#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from face.db.config import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import bcrypt


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime)

    def __init__(self, email, login, password, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.login = login
        self.password = self._hash(password)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise

    def update(self, name, surname, email, password=None):
        try:
            commit = False
            if name != self.name:
                self.name = name
                commit = True
            if surname != self.surname:
                self.surname = surname
                commit = True
            if email != self.email:
                self.email = email
                commit = True
            if password:
                self.password = self._hash(password)
                commit = True

            if commit:
                db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise

    @staticmethod
    def _hash(password):
        """Hashes the password
        :param password:
        :return:
        """
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    @classmethod
    def validate_password(cls, password, hashed):
        """Validate that the password hashes to the hashed value.
        :param hashed:
        :param password:
        :return:
        """
        return (
            password
            and hashed
            and bcrypt.hashpw(password.encode("utf8"), hashed.encode("utf8"))
            == hashed.encode("utf8")
        )


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String()
    surname = fields.String()
    email = fields.String(required=True)
    login = fields.String(required=True)
    password = fields.String(load_only=True)
    created = fields.String(dump_only=True)
    updated = fields.String(dump_only=True)
