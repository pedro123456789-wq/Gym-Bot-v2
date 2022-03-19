from flask_server import app, db
from flask import request, jsonify, make_response
from flask_server import encryption_handler




@app.route('/api', methods = ['GET'])
def home():
    return 'Api is running ...'

