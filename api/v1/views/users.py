#!/usr/bin/python3
"""Module with the view for Users objects"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, abort
import json


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Return a list of dictionaries of all users"""
    if request.method == 'GET':
        users = []
        for user in storage.all(User).values():
            users.append(user.to_dict())
        return json.dumps(users, indent=4)
    try:
        data = request.get_json()
    except Exception:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    if 'email' not in data.keys():
        return 'Missing email', 400
    if 'password' not in data.keys():
        return 'Missing password', 400
    new_user = User(**data)
    new_user.save()
    return json.dumps(new_user.to_dict(), indent=4), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_id(user_id):
    """Get a user instance from the storage"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return json.dumps(user.to_dict(), indent=4)
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'email' or k != 'created_at'\
               or k != 'updated_at':
                setattr(user, k, v)
        storage.save()
        return json.dumps(user.to_dict(), indent=4), 200