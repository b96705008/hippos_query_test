from __future__ import print_function
from __future__ import unicode_literals

import sys
import configparser
from flask import Flask
from flask import jsonify, make_response
from pymongo import MongoClient

from conf import configure_app


# config
conf_path = sys.argv[1]
config = configparser.ConfigParser()
config.read(conf_path)

# flask app
app = Flask(__name__)
_, apis = configure_app(app, config)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    HOST = config.get('client', 'host')
    PORT = config.getint('client', 'port')
    
    # journey
    for api in apis:
        print('register API: {}'.format(api['prefix']))
        app.register_blueprint(api['ctrler'], url_prefix=api['prefix'])

    app.run(debug=False, host=HOST, port=PORT, threaded=True)
