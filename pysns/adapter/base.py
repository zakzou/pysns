# -*- coding: utf-8 -*-


import liboauth2
try:
    import simplejson as json
except ImportError:
    import json

from urllib import unquote
from exception import OAuth2Error, ApiError


class Response(object):

    def __init__(self, code, result, content_type):
        self.code = code
        self.result = result
        self.content_type = content_type


class BaseOAuth2(object):
    '''
    认证包装基础类

    大部分OAuth2发生错误时候，status code都是400
    目前发现腾讯微博发生错误的时候 status code也是200
    所以需要重写方法_error_handler
    '''

    AUTHORIZATION_ENDPOINT = ''
    TOKEN_ENDPOINT = ''
    API_URL = ''

    ERROR_CODE_PARAM_NAME = ''
    ERROR_MSG_PARAM_NAME = ''


    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = liboauth2.Client(self.client_id, self.client_secret)

    def get_auth_url(self, **kwargs):
        return self.client.get_auth_url(self.AUTHORIZATION_ENDPOINT, self.redirect_uri, **kwargs)

    def get_access_token(self, code, **kwargs):
        params = dict(code=code, redirect_uri=self.redirect_uri)
        params.update(kwargs)
        resp = self.client.get_access_token(self.TOKEN_ENDPOINT, liboauth2.GRANT_TYPE_AUTH_CODE, params)
        resp = self._proc_resp(resp)
        self._error_handler(resp, OAuth2Error, self.TOKEN_ENDPOINT)
        return resp.result

    def get_user_info(self, result, **kwargs):
        raise NotImplementedError

    def fetch(self, url, params={}, http_method=liboauth2.HTTP_METHOD_GET, http_headers={}):
        url = self.API_URL + url
        resp = self.client.fetch(url, params, http_method, http_headers, liboauth2.HTTP_FORM_CONTENT_TYPE_APPLICATION)
        resp = self._proc_resp(resp)
        self._error_handler(resp, ApiError, url)
        return resp.result

    def _error_handler(self, resp, error_class, url):
        if resp.code != 200:
            errno = resp.result[self.ERROR_CODE_PARAM_NAME]
            error = resp.result[self.ERROR_MSG_PARAM_NAME]
            raise error_class('request url: %s, error code: %s, error message: %s' % (url, errno, error))

    def urldecode(self, values):
        ret = {}
        for one in values.split('&'):
            key, value = map(unquote, one.split('='))
            ret[key] = value
        return ret

    def jsondecode(self, values):
        return json.loads(values)

    def _proc_resp(self, resp):
        if resp['content_type'] and 'urlencoded' in resp['content_type']:
            resp['result'] = self.urldecode(resp['result'])
        else:
            resp['result'] = self.jsondecode(resp['result'])
        return Response(**resp)
