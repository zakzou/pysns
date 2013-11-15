# -*- coding: utf-8 -*-


from base import BaseOAuth2


class Renren(BaseOAuth2):

    AUTHORIZATION_ENDPOINT = 'https://graph.renren.com/oauth/authorize'
    TOKEN_ENDPOINT = 'https://graph.renren.com/oauth/token'
    API_URL = 'https://api.renren.com/v2'

    ERROR_CODE_PARAM_NAME = 'error'
    ERROR_MSG_PARAM_NAME = 'error_description'

    def get_user_info(self, result, **kwargs):
        self.uid = result['user']['id']
        self.access_token = result['access_token']
        self.refresh_token = result['refresh_token']
        self.expires_in = result['expires_in']

        self.client.set_access_token(self.access_token)
        result = self.fetch('/user/get', kwargs)
        self.name = result['response']['name']
        avatar = dict((x['size'], x['url']) for x in result['response']['avatar'])
        self.avatar = avatar['MAIN']
        self.avatar_large = avatar['LARGE']
