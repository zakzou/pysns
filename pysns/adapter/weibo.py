# -*- coding: utf-8 -*-


from base import BaseOAuth2


class Weibo(BaseOAuth2):

    AUTHORIZATION_ENDPOINT = 'https://api.weibo.com/oauth2/authorize'
    TOKEN_ENDPOINT = 'https://api.weibo.com/oauth2/access_token'
    API_URL = 'https://api.weibo.com/2'

    ERROR_CODE_PARAM_NAME = 'error_code'
    ERROR_MSG_PARAM_NAME = 'error'

    def get_user_info(self, result, **kwargs):
        self.uid = result['uid']
        self.access_token = result['access_token']
        self.refresh_token = ''
        self.expires_in = result['expires_in']

        self.client.set_access_token(self.access_token)
        params = dict(uid=self.uid)
        params.update(kwargs)
        result = self.fetch('/users/show.json', params)
        self.name = result['name']
        self.avatar = result['profile_image_url']
        self.avatar_large = result['avatar_large']
