# -*- coding: utf-8 -*-


from base import BaseOAuth2


class TencentWeibo(BaseOAuth2):

    AUTHORIZATION_ENDPOINT = 'https://open.t.qq.com/cgi-bin/oauth2/authorize'
    TOKEN_ENDPOINT = 'https://open.t.qq.com/cgi-bin/oauth2/access_token'
    API_URL = 'http://open.t.qq.com/api'

    ERROR_CODE_PARAM_NAME = 'errorCode'
    ERROR_MSG_PARAM_NAME = 'errorMsg'

    def _error_handler(self, resp, error_class, url):
        '''
        腾讯微博比较蛋疼
        认证和api接口的错误键不一样
        '''
        if self.ERROR_MSG_PARAM_NAME in resp.result:
            errno = resp.result[self.ERROR_CODE_PARAM_NAME]
            error = resp.result[self.ERROR_MSG_PARAM_NAME]
            raise error_class('request url: %s, error code: %s, error message: %s' % (url, errno, error))
        elif 'errcode' in resp.result:
            errno = resp.result['errcode']
            if errno:
                error = resp.result['msg']
                raise error_class('request url: %s, error code: %s, error message: %s' % (url, errno, error))

    def get_user_info(self, result, **kwargs):
        self.uid = result['openid']
        self.access_token = result['access_token']
        self.refresh_token = result['refresh_token']
        self.expires_in = result['expires_in']
        self.name = result['nick']

        self.client.set_access_token(self.access_token)
        params = dict(oauth_consumer_key=self.client_id, oauth_version='2.a', openid=self.uid, format='json')
        params.update(kwargs)
        result = self.fetch('/user/info', params)
        self.avatar = result['data']['head']
        self.avatar_large = ""
