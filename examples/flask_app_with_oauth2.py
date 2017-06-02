# coding=utf-8

from flask import Flask
from functools import wraps

from hhwebutils.flask_oauth2 import Oauth2

app = Flask(__name__)
app.debug = True

# Секретный ключ используется для подписи куки session, что позволяет безопасно использовать сессию во flask
app.config['SECRET_KEY'] = 'Really secret key! (e.g. cat from /dev/random)'

oauth2_authorizer = Oauth2(
    client_id='123',
    client_secret='456',
    access_token_url='https://hh.ru/oauth/token',
    authorize_url='https://hh.ru/oauth/authorize'
)


def authorization_error(msg):
    """Возвращает страницу с сообщением об ошибке авторизации"""
    return u'Ошибка авторизации. {}'.format(msg)


def requires_auth(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        if 'access_token' in session:
            # Пользователь авторизован
            return func(*args, **kwds)
        elif 'code' in request.args:
            # Пользователь получил временный код и хочет авторизоваться
            access_token = oauth2_authorizer.get_access_token(request.args['code'])
            if access_token is None:
                return authorization_error(u'Ошибка при получении токена')
            # access granted
            session['access_token'] = access_token
        else:
            return oauth2_authorizer.authorize()
    return wrapper


@app.route('/')
@requires_auth
def index():
    return "super secret page"


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
