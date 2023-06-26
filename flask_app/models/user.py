from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re # regex module
# Create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # staticmethod to validate a new user's data
    @staticmethod
    def is_valid_user(user_info):
        is_valid = True # we assume the is true
        if len(user_info['first_name']) <= 0:
            flash("First name is required.")
            is_valid = False
        if len(user_info['last_name']) <= 0:
            flash("Last name is required.")
            is_valid = False
        if len(user_info['email']) <= 0:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(user_info['email']):
            flash("Invalid email address.")
            is_valid = False
        return is_valid

    # classmethods used to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users2_schema').query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
        #comes back as the new row id. If the query is bad it will come back as False
        result = connectToMySQL('users2_schema').query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL('users2_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('users2_schema').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users2_schema').query_db(query, data)
