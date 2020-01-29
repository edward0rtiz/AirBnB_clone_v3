#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os import getenv
import sqlalchemy

db_storage = (getenv("HBNB_TYPE_STORAGE"), "json_file")

# GET method
@app.views.route('/places/<place_id>/amenities')
def place_amenities(place=None):
    obj_place_am = storage.get("Place", place_id)
    if  obj_place_am is None:
        abort (404)
    return jsonify([am.to_dict() for am
                    in obj_place_am.amenities])

# DELETE method
@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def amenity_review_delete(place_id=None, amenity_id=None):
    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_amenity is None or obj_place is None:
        abort(404)
    list = [item.id for item in obj_place.amenities]
    if amenity.id not in list:
        abort(404)

    if db == 'db':
        obj_place.amenities.remove(amenity)
    else:
        obj_place.amenities().remove(amenity.id)
    obj_place.save()
    return jsonify({}), 200

# POST method
@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def amenity_place(place_id, amenity_id):
    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_place is None or obj_amenity is None:
        abort(404)
    list = [item.id for item in obj_place.amenities]
    if obj_amenity.id in list:
        return jsonify(obj_amenity.to_dict()), 200

    if db is 'db':
        obj_place.amenities.append(obj_amenity)
    else:
        obj_place.amenities.append(obj_amenity.id)
    return jsonify(obj_amenity.to_dict()), 201
