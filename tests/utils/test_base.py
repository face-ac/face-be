#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from face.app import create_app
from face.db.config import db, TestingConfig


class BaseTestCase(unittest.TestCase):
    """A base test case"""

    def setUp(self):
        app = create_app(TestingConfig)
        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        db.session.close_all()
        db.drop_all()
