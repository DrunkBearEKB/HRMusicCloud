from flask import Flask, request, render_template, abort, session
from flask.app import HTTPException

from db import DBHandler


def add_main_routes(app: Flask, db: DBHandler):
    @app.route('/', methods=['GET'])
    def route_main():
        context = {
            'title': 'HRMusicCloud'
        }
        if 'Auth-Key' in session.keys():
            user_login = db.get_user_login(session['Auth-Key'])
            if user_login is not None:
                context['logged'] = True
                context['user_login'] = user_login
            else:
                session.pop('Auth-Key')
        return render_template(
            'main.html',
            **context
        )

    @app.route('/about/', methods=['GET'])
    def route_about():
        context = {
            'title': 'HRMusicCloud - About'
        }
        if 'Auth-Key' in session.keys():
            user_login = db.get_user_login(session['Auth-Key'])
            if user_login is not None:
                context['logged'] = True
                context['user_login'] = user_login
            else:
                session.pop('Auth-Key')
        return render_template(
            'about.html',
            **context
        )

    @app.route('/privacy-policy/', methods=['GET'])
    def route_privacy_policy():
        context = {
            'title': 'HRMusicCloud - Privacy Policy'
        }
        if 'Auth-Key' in session.keys():
            user_login = db.get_user_login(session['Auth-Key'])
            if user_login is not None:
                context['logged'] = True
                context['user_login'] = user_login
            else:
                session.pop('Auth-Key')
        return render_template(
            'privacy_policy.html',
            **context
        )

    @app.route('/api-reference/', methods=['GET'])
    def route_api_reference():
        context = {
            'title': 'HRMusicCloud - WEB API'
        }
        if 'Auth-Key' in session.keys():
            user_login = db.get_user_login(session['Auth-Key'])
            if user_login is not None:
                context['logged'] = True
                context['user_login'] = user_login
            else:
                session.pop('Auth-Key')
        return render_template(
            'api.html',
            **context
        )

    @app.errorhandler(HTTPException)
    def http_error_handler(error: HTTPException):
        context = {
            'title': f'HRMusicCloud - {error.code}: {error.name}',
            'error': error
        }
        return render_template(
            'error.html',
            **context
        )

    # @app.before_request
    # def before_request():
    #     if 'Auth-Key' in session.keys():
    #         auth_key = session['Auth-Key']
    #         if not db.check_user_auth_key(auth_key):
    #             session.pop('Auth-Key')
    #     # print('Session: ' +
    #     #       '; '.join([f'{k}: {session[k]}' for k in session.keys()]))

    # @app.after_request
    # def after_request(response):
    #     if 'Auth-Key' in session.keys():
    #         response.headers['Auth-Key'] = request.headers['Auth-Key']
    #     response.headers['KakaBuka'] = 'Byka'
    #     return response
