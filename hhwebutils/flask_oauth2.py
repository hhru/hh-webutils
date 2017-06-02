# coding=utf-8

from __future__ import print_function
import json
from flask import redirect
import urllib
import urllib2


class Oauth2:

    def __init__(self, client_id, client_secret, access_token_url, authorize_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url

    def authorize(self, redirect_uri=None):
        """Перенаправляет пользователя на удаленный сайт для авторизации"""
        request_args = {
                'response_type': 'code',
                'client_id': self.client_id,
        }
        if redirect_uri is not None:
            request_args['redirect_uri'] = redirect_uri
        request_args = urllib.urlencode(request_args)
        return redirect("{}?{}".format(self.authorize_url, request_args))

    def get_access_token(self, code):
        server_request_args = urllib.urlencode(
            {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
        )
        try:
            response = urllib2.urlopen(self.access_token_url, server_request_args)
            response_data = json.loads(response.read())
            access_token = response_data['access_token'] if 'access_token' in response_data else None
        except urllib2.HTTPError:
            return None
        return access_token
