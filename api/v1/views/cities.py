#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City

@app_views.route('/states/<id>/cities', methods=['GET'])
def state_id(id):
    list_cities = []
    state_obj = storage.get('State', id)
    if state_obj is None:
        abort(404)
    for city_obj in state_obj.cities:
        list_cities.append(city_obj.to_dict())
    return jsonify(list_cities)

@app_views.route('/cities/<id>', methods=['GET'])
def cities(id=None):
    list_state = []
    state_objs = storage.get('City', id)
    if not state_objs:
        abort(404)
    return jsonify(state_objs.to_dict())

@app_views.route('/cities/<id>', methods=['DELETE'])
def cities_delete(id):
    obj_city = storage.get('City', id)
    if obj_city is None:
        abort(404)
    storage.delete(obj_city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<id>', methods=['PUT'])
def city_put(id):
    obj_city = storage.get('City', id)
    do_put = request.get_json()
    if do_put is not request.is_json and do_put is None:
        abort(404, "Not a JSON")
    for k, v in do_put.items():
        if (k is not "id" and k is not "created_at" and
            k is not "updated_at" and k is not "state_id"):
            setattr(obj_city, k, v)
    obj_city.save()
    return (jsonify(obj_city.to_dict())), 200

@app_views.route('/states/<id>/cities', methods=['POST'])
def city_post(id):
    do_post = request.get_json()
    if do_post is not request.is_json:
        if "name" in do_post:
            #do_post[state_id] = id
            new_obj = City(state_id=id, **do_post)
            storage.new(new_obj)
            storage.save()
            return jsonify(new_obj.to_dict()), 201
        else:
            abort(404, "Missing name")
    else:
        abort(404, "Not a JSON")
