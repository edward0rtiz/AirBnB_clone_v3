#!/usr/bin/python3
"""HTTP methods for API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/reviews/<review_id>', methods=['GET'])
def reviews(review_id):
    """GET method for reviews"""
    obj_review = storage.get("Review", review_id)
    if obj_review is None:
        abort(404)
    else:
        return jsonify(obj_review.to_dict())


@app_views.route('/places/<place_id>/reviews')
def review_pl(place_id=None):
    list_review = []
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    else:
        for review in obj_place.list_reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)

@app_views.route('/reviews/<review_id>', methods=['DELETE', 'PUT'])
def review_del_put(review_id=None):
    """DELETE and PUT method for reviews"""
    obj_review = storage.get("Review", review_id)
    if obj_review is None:
        abort(404)
    if request.method == 'DELETE':
        obj_review.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        do_put = request.get_json()
        for k, v in do_put.items():
            if (k is not "id" and
                k is not "created_at" and
                k is not "updated_at" and
                k is not "user_id" and
                    k is not "place_id"):
                setattr(obj_review, k, v)
        obj_review.save()
        return jsonify(obj_review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_post(place_id):
    """POST method for reviews"""
    get_place = storage.get("Place", place_id)
    if get_place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'text' not in request.json:
        abort(400, "Missing text")
    do_post = request.get_json()
    user_id = do_post.get("user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_review = Review(**do_post)
    setattr(new_review, "place_id", place_id)
    storage.do_post(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201
