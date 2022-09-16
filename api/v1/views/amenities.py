#!/usr/bin/python3
"""Module with the view for Amenities objects"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import request, abort
import json


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """Return a list of dictionaries of all amenities"""
    if request.method == 'GET':
        amenities = []
        for amenity in storage.all(Amenity).values():
            amenities.append(amenity.to_dict())
        return json.dumps(amenities, indent=4)
    try:
        data = request.get_json()
    except Exception:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    new_amenity = Amenity(**data)
    new_amenity.save()
    return json.dumps(new_amenity.to_dict(), indent=4), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """Get an amenity instance from the storage"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return json.dumps(amenity.to_dict(), indent=4)
    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(amenity, k, v)
        storage.save()
        return json.dumps(amenity.to_dict(), indent=4), 200