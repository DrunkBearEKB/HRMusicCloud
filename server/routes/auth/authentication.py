from flask import Flask, request, redirect, render_template, make_response, \
    session, abort
import subprocess
import os

from db import DBHandler
from routes.auth.auth_codes import AuthCode
from utils.http_return_codes import HTTP_RETURN_CODES


def check_authentication(db: DBHandler):
    def check_authentication_decorator(func):
        def func_wrapped(*args, **kwargs):
            if 'Auth-Key' in session.keys():
                if db.check_user_auth_key(session['Auth-Key']):
                    return func(*args, **kwargs)
            session['ReferBack'] = request.url_rule.rule
            return redirect('/login/')
        func_wrapped.__name__ = func.__name__

        return func_wrapped
    return check_authentication_decorator


def check_api_authentication(db: DBHandler):
    def check_authentication_decorator(func):
        def func_wrapped(*args, **kwargs):
            if 'Auth-Key' in session.keys():
                if db.check_user_auth_key(session['Auth-Key']):
                    return func(*args, **kwargs)
            return {
                'error_code': 401,
                'info': HTTP_RETURN_CODES[401]
            }
        func_wrapped.__name__ = func.__name__

        return func_wrapped
    return check_authentication_decorator


def add_authentication_routes(app: Flask, db: DBHandler):
    @app.route('/login/', methods=['GET'])
    def route_login_get():
        if 'ReferBack' in session:
            referer = session['ReferBack']
            session.pop('ReferBack')
        else:
            referer = request.referrer
        if referer not in ['/player/', '/about/', '/privacy-policy/']:
            referer = '/'
        context = {
            'title': f'HRMusicCloud - Login',
            'referrer': referer
        }
        return make_response(render_template(
            'login.html',
            **context
        ))

    @app.route('/login/', methods=['POST'])
    def route_login_post():
        login = request.form.get('login')
        password = request.form.get('password')
        referrer = request.form.get('referrer')

        if login == 'None' or password == 'None':
            context = {
                'title': f'HRMusicCloud - Login',
                'exception': True
            }
            return render_template(
                'login.html',
                **context
            )

        user_auth_key = db.check_user_auth(
            request.form.get('login'), request.form.get('password'))

        if user_auth_key is not None:
            session['Auth-Key'] = user_auth_key
            return redirect(referrer)
        else:
            context = {
                'title': f'HRMusicCloud - Login',
                'exception': True
            }
            return render_template(
                'login.html',
                **context
            )

    @app.route('/login/forgot-password/', methods=['GET'])
    def route_login_forgot_password_get():
        context = {
            'title': f'HRMusicCloud - Forgot Password'
        }
        return render_template(
            'login_forgot_password.html',
            **context
        )

    @app.route('/login/forgot-password/', methods=['POST'])
    def route_login_forgot_password_post():
        user_email = request.form.get('email')

        if user_email == 'None':
            context = {
                'title': f'HRMusicCloud - Login',
                'exception': True
            }
            return render_template(
                'login_forgot_password.html',
                **context
            )

        context = {
            'title': f'HRMusicCloud - Forgot Password'
        }

        if db.check_user_email(user_email):
            reset_code = db.set_reset_code(user_email)

            subprocess.run(
                ['python', os.path.join(os.getcwd(), 'utils', 'send_reset_code.py'),
                 '--to', user_email, '--address', request.url_root,
                 '--code', reset_code])
            # send_reset_email(user_email, request.url_root, reset_code)
            context['mail_sent'] = True
            context['user_email'] = user_email
        else:
            context['exception'] = True

        return render_template(
            'login_forgot_password.html',
            **context
        )

    @app.route('/login/reset-password/<string:reset_code>', methods=['GET'])
    def route_login_reset_password_get(reset_code: str):
        context = {
            'title': f'HRMusicCloud - Reset Password'
        }

        user_id = db.check_reset_code(reset_code)
        if user_id is None:
            return abort(404)

        return render_template(
            'login_reset_password.html',
            **context
        )

    @app.route('/login/reset-password/<string:reset_code>', methods=['POST'])
    def route_login_reset_password_post(reset_code: str):
        password = request.form.get('password')

        if db.set_user_password(reset_code, password):
            return redirect('/login/')
        return abort(404)

    @app.route('/register/', methods=['GET'])
    def route_register_get():
        context = {
            'title': f'HRMusicCloud - Register'
        }
        return render_template(
            'register.html',
            **context
        )

    @app.route('/register/', methods=['POST'])
    def route_register_post():
        login = request.form.get('login')
        password = request.form.get('password')
        email = request.form.get('email')

        if login == 'None' or password == 'None' or email == 'None':
            context = {
                'title': f'HRMusicCloud - Login',
                'exception': True
            }
            return render_template(
                'register.html',
                **context
            )

        code = db.add_user(login, password, email, b'')
        if code == AuthCode.Ok:
            return redirect('/login')
        elif code == AuthCode.Exists:
            return

    @app.route('/profile/<string:user_login>', methods=['GET'])
    def route_profile(user_login: str):
        context = {
            'title': f'HRMusicCloud - {user_login}'
        }
        if 'Auth-Key' in session.keys():
            user_login = db.get_user_login(session['Auth-Key'])
            if user_login is not None:
                context['logged'] = True
                context['user_login'] = user_login
            else:
                session.pop('Auth-Key')
                abort(404)
        else:
            abort(404)

        login, email, birth, country = db.get_user(session['Auth-Key'])

        context['login'] = user_login
        context['email'] = email
        context['birth'] = birth
        context['country'] = country

        return render_template(
            'profile.html',
            **context
        )
