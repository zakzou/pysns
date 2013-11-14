# -*- coding: utf-8 -*-


import liboauth2

from base import BaseOAuth2


class Douban(BaseOAuth2):

    AUTHORIZATION_ENDPOINT = 'https://www.douban.com/service/auth2/auth'
    TOKEN_ENDPOINT = 'https://www.douban.com/service/auth2/token'
    API_URL = 'https://api.douban.com/v2'

    ERROR_CODE_PARAM_NAME = 'code'
    ERROR_MSG_PARAM_NAME = 'msg'

    def get_user_info(self, result, **kwargs):
        self.uid = result['douban_user_id']
        self.access_token = result['access_token']
        self.refresh_token = result['refresh_token']
        self.expires_in = result['expires_in']

        self.client.set_access_token(self.access_token)
        self.client.set_access_token_type(liboauth2.ACCESS_TOKEN_BEARER)
        result = self.fetch('/user/~me', kwargs)
        self.name = result['name']
        self.avatar = result['avatar']
        self.avatar_large = ""
