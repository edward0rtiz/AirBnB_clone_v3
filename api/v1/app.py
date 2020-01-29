#!/usr/bin/python3
""" app.py file """
import os
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')
app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(cls):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """error 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    """Initialize api"""
    app.run(host=host, port=int(port), threaded=True)
