"""
SFU CMPT 756
Sample application---user service.
"""

# Standard library modules
import logging
import sys
import time

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

import jwt

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Bestseller process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


# @bp.route('/', methods=['GET'])
# @metrics.do_not_track()
# def hello_world():
#     return ("If you are reading this in a browser, your service is "
#             "operational. Switch to curl/Postman/etc to interact using the "
#             "other HTTP verbs.")


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/<bestseller_id>', methods=['PUT'])
def update_bestseller(bestseller_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        title = content['title']
        copies = content['copies']
        rating = content['rating']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "bestseller", "objkey": bestseller_id},
        json={"title": title,
              "copies": copies,
              "rating": rating})
    return (response.json())


@bp.route('/', methods=['POST'])
def create_bestseller():
    """
    Create a bestseller.
    If a record already exists with the same title, copies and rating,
    the old b_id is replaced with a new one.
    """
    try:
        content = request.get_json()
        title = content['Title']
        copies = content['Copies']
        rating = content['Rating'] if 'Rating' in content else None
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][1]
    payload = {"objtype": "bestseller",
               "Title": title,
               "Copies": copies}
    if rating is not None:
        payload["Rating"] = rating
    response = requests.post(
        url,
        json=payload)
    return (response.json())


@bp.route('/<bestseller_id>', methods=['DELETE'])
def delete_bestseller(bestseller_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/' + db['endpoint'][2]

    response = requests.delete(url,
                               params={"objtype": "bestseller",
                                       "objkey": bestseller_id})
    return (response.json())


@bp.route('/<bestseller_id>', methods=['GET'])
def get_bestseller(bestseller_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(
            json.dumps({"error": "missing auth"}),
            status=401,
            mimetype='application/json')
    payload = {"objtype": "bestseller", "objkey": bestseller_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/', methods=['GET'])
def list_all():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/list'
    response = requests.get(
        url,
        params={"objtype": "bestseller"},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/login', methods=['PUT'])
def login():
    try:
        content = request.get_json()
        uid = content['uid']
    except Exception:
        return json.dumps({"message": "error reading parameters"})
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(url, params={"objtype": "bestseller",
                            "objkey": uid})
    data = response.json()
    if len(data['Items']) > 0:
        encoded = jwt.encode({'bestseller_id': uid, 'time': time.time()},
                             'secret', algorithm='HS256')
    return encoded


@bp.route('/logoff', methods=['PUT'])
def logoff():
    try:
        content = request.get_json()
        _ = content['jwt']
    except Exception:
        return json.dumps({"message": "error reading parameters"})
    return {}


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/bestseller/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
