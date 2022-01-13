import os
import sys
from flask import Flask, abort, send_from_directory

from db import DBHandler
from routes.auth.authentication import check_api_authentication


def add_album_routes(app: Flask, db: DBHandler):
    @app.route('/api/album/<string:album_id>/info/', methods=['GET'])
    @check_api_authentication(db)
    def route_album_info_get(album_id: str):
        result = db.get_album_info(album_id)
        return abort(404) if result is None else {
            'album_id': album_id,
            'info': result
        }

    @app.route('/api/album/<string:album_id>/image/', methods=['GET'])
    @check_api_authentication(db)
    def route_album_image_get(album_id: str):
        result = db.get_album_picture_path(album_id)
        if result is None:
            abort(404)
        if sys.platform != 'win':
            result = result.replace('\\', '/')
        _dir, _name = os.path.dirname(result), os.path.basename(result)
        return send_from_directory(
            _dir, path=_name, attachment_filename=_name
        )

    @app.route('/api/album/<string:album_id>/artists/', methods=['GET'])
    @check_api_authentication(db)
    def route_album_artists_get(album_id: str):
        result = db.get_album_artists(album_id)
        return abort(404) if result is None else {
            'album_id': album_id,
            'artists': result
        }

    @app.route('/api/album/<string:album_id>/tracks/', methods=['GET'])
    @check_api_authentication(db)
    def route_album_tracks_get(album_id: str):
        result = db.get_album_tracks(album_id)
        return abort(404) if result is None else {
                'album_id': album_id,
                'tracks': result
            }
