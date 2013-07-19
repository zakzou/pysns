# -*- coding: utf-8 -*-


import pysns
import settings

from flask import Flask, request, redirect



app = Flask(__name__)
app.debug = True


@app.route('/user/<string:sitename>/authorize/')
def user_authorize(sitename):
    try:
        configs = settings.THIRD_PARTY_OAUTH2[sitename]
        state = request.args.get('state', '')
    except Exception:
        pass
    client = pysns.get_client(sitename, **configs)
    return redirect(client.get_auth_url(state=state))


@app.route('/user/<string:sitename>/callback/')
def user_callback(sitename):
    args = request.args
    try:
        code = args['code']
        configs = settings.THIRD_PARTY_OAUTH2[sitename]
    except Exception:
        pass
    client = pysns.get_client(sitename, **configs)
    result = client.get_access_token(code)
    client.get_user_info(result, access_token=result['access_token'])
    print client.name
    print client.uid
    print client.avatar
    return 'ok'


if __name__ == '__main__':
    app.run()
