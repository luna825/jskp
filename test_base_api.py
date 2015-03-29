# coding=utf-8
import kp_base_api

consumer_key ="xcSj3bB3qBBzfdew"
consumer_secret = "rgFU71RflLetSobJ"

oauth_token="0124a4c75f53ec296d2946c2"
oauth_token_secret="77dfb534106c47c991afaf64edc7f6bb"

root = "app_folder"
path = "/filed"

#print kp_base_api.get_account_info(consumer_key,consumer_secret,oauth_token,oauth_token_secret)
print kp_base_api.get_metadata(consumer_key,consumer_secret,oauth_token,oauth_token_secret,root,path)