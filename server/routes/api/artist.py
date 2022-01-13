import os
import sys
from flask import Flask, abort, send_from_directory

from db import DBHandler
from routes.auth.authentication import check_api_authentication


def add_artist_routes(app: Flask, db: DBHandler):
    @app.route('/api/artist/<string:artist_id>/info/', methods=['GET'])
    @check_api_authentication(db)
    def route_artist_info_get(artist_id: str):
        result = db.get_artist_info(artist_id)
        return abort(404) if result is None else {
            'artist_id': artist_id,
            'info': result
        }

    @app.route('/api/artist/<string:artist_id>/image/', methods=['GET'])
    @check_api_authentication(db)
    def route_artist_image_get(artist_id: str):
        result = db.get_artist_picture_path(artist_id)
        if result is None:
            abort(404)
        if sys.platform != 'win':
            result = result.replace('\\', '/')
        _dir, _name = os.path.dirname(result), os.path.basename(result)
        return send_from_directory(
            _dir, path=_name, attachment_filename=_name
        )

    @app.route('/api/artist/<string:artist_id>/albums/', methods=['GET'])
    @check_api_authentication(db)
    def route_artist_albums_get(artist_id: str):
        result = db.get_artist_albums(artist_id)
        return abort(404) if result is None else {
            'artist_id': artist_id,
            'albums': result
        }

    @app.route('/api/artist/<string:artist_id>/tracks/', methods=['GET'])
    @check_api_authentication(db)
    def route_artist_tracks_get(artist_id: str):
        result = db.get_artist_tracks(artist_id)
        return abort(404) if result is None else {
            'artist_id': artist_id,
            'tracks': result
        }
