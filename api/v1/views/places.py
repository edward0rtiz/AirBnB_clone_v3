#!/usr/bin/python3
"""HTTP methods for RESTFul API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>')
def get_places(place_id=None):
    """GET place method"""
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places')
def all_place(city_id=None):
    """GET places within cities"""
    list_places = []
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    else:
        for place_city in city_obj:
            list_places.append(place_city.to_dict())
        return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['DELETE', 'PUT'])
def place(place_id=None):
    """'DELETE' methods"""
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    if request.method == 'DELETE':
        obj_place.delete()
        storage.save()
        return jsonify({}), 200
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.is_json:
        abort(400, "Missing user_id")
    if 'name' not in request.is_json:
        abort(400, "Missing name")
    do_post = request.get_json()
    new_usr = do_post.get("user_id")
    if storage.get("User", user_id) is None:
        abort(404)
    new_place = Place(**do_post)
    setattr(new_place, "city_id", city_id)
    storage.do_post(new_place)
    storage.save()
    return jsonify(place.to_dict()), 201
