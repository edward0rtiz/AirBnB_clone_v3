#!/usr/bin/python3
"""module state"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/<id>')
@app_views.route('/states')
def state(id=None):
    """state"""
    list_state = []
    if id:
        state_objs = storage.get('State', id)
        if state_objs is None:
            abort(404)
        else:
            return jsonify(state_objs.to_dict())
    for state_objs in storage.all('State').values():
            list_state.append(state_objs.to_dict())
    return jsonify(list_state)


@app_views.route('/states/<id>', methods=['GET', 'DELETE', 'PUT'])
def state_delete(id=None):
    """state delete"""
    obj_state = storage.get('State', id)
    if not obj_state:
        abort(404)
    if request.method == 'PUT':
        do_put = request.get_json()
        if not do_put:
            abort(400, "Not a JSON")
        [setattr(obj_state, k, v) for k, v in do_put.items()
        if k not in ["id", "created_at", "updated_at"]]
    obj_state.save()
    if request.method == 'DELETE':
        obj_state.delete()
        storage.save()
        return jsonify({}), 200
    return jsonify(obj_state.to_dict()), 200


@app_views.route('/states', methods=['POST'])
def state_post():
    """state post"""
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
