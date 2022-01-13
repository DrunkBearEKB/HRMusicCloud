import os
import sys
from flask import Flask, abort, send_from_directory, request

from db import DBHandler
from routes.auth.authentication import check_api_authentication


def add_search_routes(app: Flask, db: DBHandler):
    @app.route('/api/search/', methods=['GET'])
    @check_api_authentication(db)
    def route_search_get():
        if 'text' not in request.args:
            return {
                'artists': [],
                'albums': [],
                'playlists': [],
                'tracks': []
            }
        search_string = request.args['text']
        result = db.get_search_results(search_string)

        return result
