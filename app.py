#!/usr/bin/env python3
from flask import Flask, request, jsonify
import logging
from traceback import format_exc
import recommender
import uuid
from time import time, strftime

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify(message="Hello! This is the recommender system")


@app.route('/recommend', methods=['POST'])
def predict_intent():
    """
        POC of a recommendation api based on a catalog dataset.
    """

    start_time = time()
    request.json["request_id"] = uuid.uuid4().hex
    app.logger.info(f"Request: {request.json['request_id']}. Processing request '/recommend': {request.json}")

    # Prime filters
    uniq_id = request.json.get('uniq_id')
    if not uniq_id:
        message = f'Request: {request.json["request_id"]}. Missing uniq_id in request'
        delta = time() - start_time
        app.logger.error(f"{message} Elapsed time: {delta} secs")
        return jsonify(message=message), 404
    

    result, code = recommender.get_recommendation(uniq_id)

    delta = time() - start_time
    app.logger.info(f"Request: {request.json['request_id']}. Endpoint response '/recommend': {result}. Elapsed time: {delta} secs")
    return jsonify(result), code


@app.errorhandler(404)
def non_found(e):
    return jsonify(message=f"Yeah... no. '{request.full_path}' not found."), 404


@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = format_exc()
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return jsonify(message="Internal Server Error"), 500


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0')
