#!/usr/bin/python3
"""City for RESTFul API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def state_id(state_id=None):
    """state, cities  id get"""
    list_cities = []
    state_obj = storage.get('State', str(state_id))
    if state_obj is None:
        abort(404)
    else:
        for city_obj in storage.all("City").values():
            list_cities.append(city_obj.to_dict())
        return jsonify(list_cities)


@app_views.route('/cities/<id>', methods=["GET"])
def cities(id=None):
    """citie get"""
    state_objs = storage.get("City", id)
    if not state_objs:
        abort(404)
    else:
        return jsonify(state_objs.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def cities_delete(city_id=None):
    """ delete city"""
    obj_city = storage.get('City', city_id)
    if obj_city is None:
        abort(404)
    obj_city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<id>', methods=['PUT'])
def city_put(id):
    """ city put"""
    obj_city = storage.get('City', id)
    if obj_city is None:
        abort(404)
    do_put = request.get_json()
    if not do_put:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in do_put.items():
        if k is not "id" and k is not "created_at":
            if k is not "updated_at" and k is not "state_id":
                setattr(obj_city, k, v)
    obj_city.save()
    return jsonify(obj_city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_post(state_id):
    """ city post"""
    obj_state = storage.get("State", state_id)
    do_post = request.get_json()
    if obj_state is None:
        abort(404)
    if do_post is not request.is_json:
        if "name" in do_post:
            new_obj = City(**do_post)
            setattr(new_obj, "state_id", state_id)
            storage.new(new_obj)
            storage.save()
            return jsonify(new_obj.to_dict()), 201
        else:
            return jsonify({"error": "Missing name"}), 400
    else:
        return jsonify({"error": "Not a JSON"}), 400
