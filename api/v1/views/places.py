#!/usr/bin/python3
"""HTTP methods for RESTFul API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place(place_id=None):
    """ GET, 'PUT, 'DELETE'"""
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    if request.method == 'DELETE':
        obj_place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        do_put = request.get_json()
        if obj_place is not request.is_json and do_put is None:
            abort(400, "Not a JSON")
        obj_place.pop('id', None)
        obj_place.pop('created_at', None)
        obj_place.pop('updated_at', None)
        obj_place.pop('user_id', None)
        obj_place.pop('city_id', None)
        for k, v in do_out.items():
            setattr(obj_place, k, v)
        obj_place.save()
    return jsonify(obj_place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id=None):
    """POST method"""
    get_city = storage.get("City", city_id)
    if get_city is None:
        abort(404)

    do_post = request.get_json()
    if do_post is not request.is_json:
        abort(400, "Not a JSON")
    user_id = do_post.get("user_id", None)
    if user_id is not request.is_json:
        abort(400, "Missing user_id")
    name = do_post.get("name", None)
    if name is not request.is_json:
        abort(400, "Missing name")

    do_post.pop('id', None)
    do_post.pop('created_at', None)
    do_post.pop('updated_at', None)
    do_post.pop({'city_id': city_id})

    if storage.get("User", user_id) is None:
        abort(404)
    for place in storage.all("Place").values():
        if place.name == name and place.user_id == user_id:
            for k, v in do_post.items():
                setattr(place, k, v)
            place.save()
            return jsonify(place.to_dict()), 200
    new_place = Place(**do_post)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/cities/<city_id>/places')
def all_place(city_id=None):
    """CREATE places."""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    all_p = storage.all("Place").values()
    places = [place.to_dict() for place in all_p if place.city_id == city_id]
    return jsonify(places)
