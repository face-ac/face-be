#!/usr/bin/python
# -*- coding: utf-8 -*-

from face.db.models.user import User
from face.db.config import db
from faker import Faker

fake = Faker()


def create_users(num=1):
    """
    :param num: int, number of user to create
    :return: [List: User]
    """
    users = [
        {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "email": fake.ascii_company_email(),
            "login": fake.user_name(),
            "password": fake.bban(),
        }
        for _ in range(0, num)
    ]
    for user in users:
        User(
            name=user["name"],
            surname=user["surname"],
            email=user["email"],
            login=user["login"],
            password=user["password"],
        ).create()
    return users


def delete_users(users):
    db.session.query(User).filter(
        User.login.in_([user["login"] for user in users])
    ).delete(synchronize_session=False)
    db.session.commit()
