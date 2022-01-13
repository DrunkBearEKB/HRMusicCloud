import os
import sys
from flask import Flask, abort, send_from_directory

from db import DBHandler
from routes.auth.authentication import check_api_authentication


def add_track_routes(app: Flask, db: DBHandler):
    @app.route('/api/track/<string:track_id>/', methods=['GET'])
    @check_api_authentication(db)
    def route_track_get(track_id: str):
        result = db.get_track_path(track_id)
        if result is None:
            abort(404)
        if sys.platform != 'win':
            result = result.replace('\\', '/')
        _dir, _name = os.path.dirname(result), os.path.basename(result)
        return send_from_directory(
            _dir, path=_name, attachment_filename=_name[4:]
        )

    @app.route('/api/track/<string:track_id>/info/', methods=['GET'])
    @check_api_authentication(db)
    def route_track_info_get(track_id: str):
        result = db.get_track_info(track_id)
        return abort(404) if result is None else {
            'track_id': track_id,
            'info': result
        }

    @app.route('/api/track/<string:track_id>/artists/', methods=['GET'])
    @check_api_authentication(db)
    def route_track_artist_get(track_id: str):
        result = db.get_track_artists(track_id)
        return abort(404) if result is None else {
            'track_id': track_id,
            'artists': result
        }

    @app.route('/api/track/<string:track_id>/album/', methods=['GET'])
    @check_api_authentication(db)
    def route_track_album_get(track_id: str):
        result = db.get_track_album(track_id)
        return abort(404) if result is None else {
            'track_id': track_id,
            'album': result
        }
