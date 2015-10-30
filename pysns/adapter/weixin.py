# -*- coding: utf-8 -*-


from base import BaseOAuth2, to_ascii


class Weixin(BaseOAuth2):

    AUTHORIZATION_ENDPOINT = 'https://open.weixin.qq.com/connect/qrconnect'
    TOKEN_ENDPOINT = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    API_URL = 'https://api.weixin.qq.com'

    ERROR_CODE_PARAM_NAME = 'errcode'
    ERROR_MSG_PARAM_NAME = 'errmsg'

    def __init__(self, client_id, client_secret, redirect_uri):
        super(Weixin, self).__init__(client_id, client_secret, redirect_uri)
        self.client.key_map = dict(client_id='appid', client_secret='secret')

    def get_user_info(self, result, **kwargs):
        unionid = result.get('unionid')
        if unionid:
            self.uid = unionid
        else:
            self.uid = result['openid']
        self.access_token = result['access_token']
        self.refresh_token = result['refresh_token']
        self.expires_in = result['expires_in']

        self.client.set_access_token(self.access_token)
        params = dict(openid=self.uid)
        params.update(kwargs)
        result = self.fetch("/sns/userinfo", params)
        self.name = to_ascii(result['nickname'])
        self.gender = result['sex']
        self.avatar = result['headimgurl']
        self.avatar_large = result['headimgurl']
        self.country = to_ascii(result['country'])
        self.province = to_ascii(result['province'])
        self.city = to_ascii(result['city'])
