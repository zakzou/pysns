# -*- coding: utf-8 -*-


from base import BaseOAuth2, to_ascii


class Weibo(BaseOAuth2):

    AUTHORIZATION_ENDPOINT = 'https://api.weibo.com/oauth2/authorize'
    TOKEN_ENDPOINT = 'https://api.weibo.com/oauth2/access_token'
    API_URL = 'https://api.weibo.com/2'

    ERROR_CODE_PARAM_NAME = 'error_code'
    ERROR_MSG_PARAM_NAME = 'error'

    _gender_dict = dict(m=1, f=2, n=1)

    def get_user_info(self, result, **kwargs):
        self.uid = result.get('uid')
        self.access_token = result['access_token']
        self.refresh_token = result.get('refresh_token')
        self.expires_in = result.get('expires_in')

        self.client.set_access_token(self.access_token)
        params = dict(uid=self.uid)
        params.update(kwargs)
        result = self.fetch('/users/show.json', params)
        self.name = to_ascii(result['name'])
        self.gender = _gender_dict[result['gender']]
        self.avatar = result['profile_image_url']
        self.avatar_large = result['avatar_large']
        self.country = ""
        loclist = to_ascii(result.get('location', '')).split(' ')
        self.province = ""
        self.city = ""
        if len(loclist) == 2:
            self.country = "中国"
            self.province = loclist[0]
            self.city = loclist[1]
        if not self.uid:
            self.uid = result['uid']
