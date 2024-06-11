#!/usr/bin/python3
"""
Start API
"""
import os
import models
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify
from flasgger import Swagger
from flask_cors import CORS
from flasgger.utils import swag_from

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    return storage.close()


@app.errorhandler(404)
def error(error):
    """
    display 404 error message on error encounter
    """
    return jsonify({"error": "Not found"}), 404


app.config['SWAGGER'] = {
        'title': 'AirBnB clone Restful API',
        'uiversion': 3
        }

Swagger(app)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
