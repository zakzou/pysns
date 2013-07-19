pysns
================

python第三方认证登录包


特性
===============

* 方便扩展(只需重写一个方法)
* 支持常见网站（腾讯微博，新浪微博，人人，豆瓣）
* 支持mac认证


安装
================


```shell
easy_install pysns
```

或者

```shell
pip install pysns
```

或者

```shell
git clone http://git.oschina.net/zakzou/pysns.git
cd pysns
sudo python setup.py install
```


快速开始
================

### 1.1 获取oauth2客户端

```python
import pysns


Douban = pysns.get_client_class('douban')
client = Douban('client_id', 'client_secret', 'you redirect uri')
```

或者你也可以

```python
import pysns


client = pysns.get_client('douban', 'client_id', 'client_secret', 'redirect_uri')
```


### 1.2 获取认证地址

```python
auth_url = client.get_auth_url()
// auth_url = client.get_auth_url(state=state, scope=scope)
```


### 1.3 根据code获取acess token

```python
result = client.get_access_token(code)
client.get_user_info(result)
```

### 1.4 查看用户信息

```pyton
client.uid
client.name
client.access_token
client.expires_in
client.refresh_token
client.avatar
client.avatar_large
```


示例
============

查看`example/app.py`


许可证
===============

MIT: http://rem.mit-license.org
