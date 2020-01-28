#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states/<id>', methods=['GET'])
@app_views.route('/states', methods=['GET'])
def state(id=None):
    list_state = []
    if id != None:
        state_objs = storage.get('State', id)
        if not state_objs:
            abort(404)
        return jsonify(state_objs.to_dict())
    else:
        state_objs = storage.all("State")
        for states in state_objs.values():
            list_state.append(states.to_dict())
        return jsonify(list_state)

@app_views.route('/states/<id>', methods=['DELETE'])
def state_delete(id):
    obj_state = storage.get('State', id)
    if obj_state is None:
        abort(404)
    storage.delete(obj_state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<id>', methods=['PUT'])
def state_put(id):
    obj_state = storage.get('State', id)
    do_put = request.get_json()
    if do_put is not request.is_json and do_put is None:
        abort(404, "Not a JSON")
    for k, v in do_put.items():
        if (k is not "id" and k is not "created_at" and
            k is not "updated_at"):
            setattr(obj_state, k, v)
    obj_state.save()
    return (jsonify(obj_state.to_dict())), 200

@app_views.route('/states', methods=['POST'])
def state_post():
    do_post = request.get_json()
    if do_post is not request.is_json:
        if "name" in do_post:
            new_obj = State(**do_post)
            storage.new(new_obj)
            storage.save()
            return jsonify(new_obj.to_dict()), 201
        else:
            abort(404, "Missing name")
    else:
        abort(404, "Not a JSON")
