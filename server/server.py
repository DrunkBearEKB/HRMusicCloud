import sys
import socket
from flask import Flask
import configparser
import traceback

from routes import add_routes
from db import load_db


PATH_CONFIG_FILE = 'config.ini'


def parse_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG_FILE)

    return config


def main() -> None:
    config = parse_config()

    app = Flask(__name__)
    db = load_db()
    add_routes(app, db)

    try:
        app.secret_key = config['Settings.WebServer']['secret_key'].encode()

        server_parameters = {
            'host': socket.gethostbyname(socket.gethostname()),
            'port': int(config['Settings.WebServer']['port'])
        }
        if config.getboolean('Settings.WebServer', 'run_over_https'):
            server_parameters['ssl_context'] = ('cert.pem', 'key.pem')
    except (ValueError, IndexError):
        traceback.print_exc()
        sys.exit()

    app.run(**server_parameters)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
