#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from tests.utils.db_operation import create_users, delete_users
from tests.utils.test_base import BaseTestCase
from faker import Faker

fake = Faker()


class TestUser(BaseTestCase):
    users = None

    def setUp(self):
        super(TestUser, self).setUp()
        self.users = create_users()

    def tearDown(self):
        delete_users(self.users)

    def test_create_user(self):
        user = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "email": fake.ascii_company_email(),
            "login": fake.user_name(),
            "password": fake.bban(),
        }
        response = self.app.post(
            "/api/user", data=json.dumps(user), content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("user" in data)
        self.users.append(user)

    def test_login_invalid(self):
        login = {"login": "invalid_username", "password": "invalid_password"}
        response = self.app.post(
            "/api/login", data=json.dumps(login), content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("message" in data)

    def test_login_valid(self):
        login = {"login": self.users[0]["login"], "password": self.users[0]["password"]}
        response = self.app.post(
            "/api/login", data=json.dumps(login), content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("user" in data)
