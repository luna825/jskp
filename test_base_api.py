# coding=utf-8
import kp_base_api

consumer_key ="xcSj3bB3qBBzfdew"
consumer_secret = "rgFU71RflLetSobJ"

(no_oauth_token,no_oauth_token_secret) = kp_base_api.request_token(consumer_key,consumer_secret)
print u'请访问下面地址进行授权：'
print kp_base_api.get_authorize_url(no_oauth_token)
authorization_key = raw_input(u'请输入你的授权码：')
print kp_base_api.request_access_token(consumer_key,consumer_secret,
	no_oauth_token,no_oauth_token_secret)