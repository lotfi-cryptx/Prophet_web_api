from typing import Set
from fbprophet import Prophet

import os
import hashlib


class Model:
    model_id: int = -1
    model_name: str = ""
    model_description: str = ""
    model: Prophet


class User:

    class ModelNotFound(Exception):
        pass

    username: str = ""
    hashed_password: str = ""
    models: Set[Model] = set()
    last_id: int = 0

    def __init__(self, username: str, hashed_password: str) -> None:
        self.username = username
        self.hashed_password = hashed_password
        self.last_id = 0
        return

    def add_model(self, model_name: str, model_description: str, model: Prophet) -> int:

        m = Model()
        m.model_id = self.last_id + 1
        m.model_name = model_name
        m.model_description = model_description
        m.model = model

        self.models.add(m)

        self.last_id = self.last_id + 1

        return m.model_id

    def get_model(self, model_id) -> Model:

        for model in self.models:
            if model_id == model.model_id:
                return model

        raise User.ModelNotFound



class DB:

    salt = os.urandom(32)
    users: Set[User] = set()


    class UserAlreadyExists(Exception):
        pass

    class UserNotFound(Exception):
        pass


    def __init__(self) -> None:
        pass


    def add_user(self, username: str, password: str) -> None:

        for user in self.users:
            if username == user.username:
                raise DB.UserAlreadyExists
        
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000)

        new_user = User(username, hashed_password)
        self.users.add(new_user)


    def verify_user(self, username: str, password: str) -> bool:

        for user in self.users:
            if username == user.username:

                hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000)

                if hashed_password == user.hashed_password:
                    return True

                return False

        raise DB.UserNotFound


    def get_user(self, username: str) -> User:

        for user in self.users:
            if username == user.username:
                return user

        raise DB.UserNotFound