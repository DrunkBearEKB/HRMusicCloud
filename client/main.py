import sys
import os
import socket
from seleniumwire import webdriver
import webbrowser
import configparser
import time


PATH_CONFIG_FILE = 'config.ini'


def create_default_config():
    with open(PATH_CONFIG_FILE, mode='w') as file:
        file.write(
            '[Settings.Authentication]\n'
            'auth_key = '
        )


def parse_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if not os.path.exists(PATH_CONFIG_FILE):
        create_default_config()
    config.read(PATH_CONFIG_FILE)

    return config


def main():
    config = parse_config()

    try:
        address = config['Settings.Authentication']['address'] \
            if config['Settings.Authentication']['address'] != '' \
            else f'{socket.gethostbyname(socket.gethostname())}:80'
    except KeyError:
        address = f'{socket.gethostbyname(socket.gethostname())}:80'

    try:
        auth_key = config['Settings.Authentication']['auth_key']
        if auth_key == '':
            raise KeyError
    except KeyError:
        create_default_config()
        webbrowser.open(f'http://{address}/login/')
        return

    chromedriver = r'C:\Users\Григорий\Downloads\chromedriver.exe'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    # def interceptor(request):
    #     del request.headers['Auth-Key']
    #     request.headers['Auth-Key'] = auth_key
    #
    # driver.request_interceptor = interceptor

    try:
        # driver.add_cookie({'Auth-Key': auth_key})
        driver.get(f'http://{address}/player/')
        while True:
            time.sleep(3600)
    except:
        pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
