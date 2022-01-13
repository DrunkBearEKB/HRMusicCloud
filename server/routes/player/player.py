import flask
from flask import Flask, make_response, render_template, request, abort, \
    session

from db import DBHandler
from routes.auth.authentication import check_authentication, \
    check_api_authentication


def add_player_routes(app: Flask, db: DBHandler):
    @app.route('/player/', methods=['GET'])
    @check_authentication(db)
    def route_player():
        response = make_response(render_template(
            'player.html',
            title='HRMusicCloud - WebPlayer'
        ))
        response.headers.set('user_id', db.get_user_id(session['Auth-Key']))
        return response

    @app.route('/user/<string:user_id>/last_track_id/', methods=['GET'])
    @check_api_authentication(db)
    def route_user_last_track_id_get(user_id: str):
        result = db.get_user_last_track_id(user_id)
        return abort(404) if result is None else {
            'user_id': user_id,
            'last_track_id': result
        }

    @app.route('/user/<string:user_id>/', methods=['POST'])
    @check_api_authentication(db)
    def route_user_last_track_id_post(user_id: str):
        if 'last_track_id' not in request.args:
            return {
                'status': 'Failed'
            }
        db.update_user_last_track_id(user_id, request.args['last_track_id'])
        print(f'Updated user_id={user_id} last_track_id={request.args["last_track_id"]}')
        return {
            'status': 'Ok'
        }
