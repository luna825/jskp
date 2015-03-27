# coding=utf-8

import os
import sys
import locale
SystemLanguageCode, SystemEncoding = locale.getdefaultlocale()
if SystemEncoding and not sys.platform.startswith('win32'):
	sysenc = SystemEncoding.upper()
	if sysenc != 'UTF-8' and sysenc != 'UTF8':
		err = "You MUST set system locale to 'UTF-8' to support unicode file names.\n" + \
			"Current locale is '{}'".format(SystemEncoding)
		ex = Exception(err)
		print(err)
		raise ex

if not SystemEncoding:
	# ASSUME UTF-8 encoding, if for whatever reason,
	# we can't get the default system encoding
	print("*WARNING*: Cannot detect the system encoding, assume it's 'UTF-8'")
	SystemEncoding = 'utf-8'

import codecs
# no idea who is the asshole that screws the sys.stdout.encoding
# the locale is 'UTF-8', sys.stdin.encoding is 'UTF-8',
# BUT, sys.stdout.encoding is None ...
if not (sys.stdout.encoding and sys.stdout.encoding.lower() == 'utf-8'):
	encoding_to_use = sys.stdout.encoding
	try:
		codecs.lookup(encoding_to_use)
		u'汉字'.encode(encoding_to_use)
	except: # (LookupError, TypeError, UnicodeEncodeError):
		encoding_to_use = 'utf-8'
	sys.stdout = codecs.getwriter(encoding_to_use)(sys.stdout)
	sys.stderr = codecs.getwriter(encoding_to_use)(sys.stderr)


import webbrowser
import kp_base_api
import re

token_saved_to ="./authorized.data"

class kp_demo():
	consumer_key = "xcSj3bB3qBBzfdew"
	consumer_secret = "rgFU71RflLetSobJ"
	root = u"金山快盘python"

	def __init__(self):
		self.oauth_token=""
		self.oauth_token_secret=""
		self.load_authorized_token()
	def load_authorized_token(self):
		try:
			lines = open(token_saved_to).readlines()
			for line in lines:
				g = re.match("oauth_token\s*=\s*(\w+)",line)
				if g :
					self.oauth_token = g.group(1)
				else:
					g = re.match("oauth_token_secret\s*=\s*(\w+)",line)
					if g :
						self.oauth_token_secret = g.group(1)
			if len(self.oauth_token)>0 and len(self.oauth_token_secret)>0:
				return True
			else:
				return False
		except:
			return False
	def save_authorized_token(self,oauth_token,oauth_token_secret):
		self.oauth_token = oauth_token
		self.oauth_token_secret = oauth_token_secret
		open(token_saved_to,"w").write("oauth_token=%s\noauth_token_secret=%s"\
		 %(oauth_token,oauth_token_secret))
	def is_authorized(self):
		return len(self.oauth_token)>0 and len(self.oauth_token_secret)>0
	def authorized(self):
		try:
			oauth_token,oauth_token_secret = kp_base_api.request_token(kp_demo.consumer_key,
				kp_demo.consumer_secret)
			authorized_url = kp_base_api.get_authorize_url(oauth_token)
			webbrowser.open(authorized_url)
			inputed = raw_input(u"请在打的页面里，给些程序授权。\n已经授权了吗？(Y/N默认为N)")
			if inputed == "" or inputed=="Y" or inputed == "y":
				authorized_oauth_token_secret,authorized_oauth_token,user_id,charged_dir=\
					kp_base_api.request_access_token( kp_demo.consumer_key, kp_demo.consumer_secret, oauth_token, oauth_token_secret)
				self.save_authorized_token(authorized_oauth_token,authorized_oauth_token_secret)
				print u"授权成功!"
			else:
				print u"授权失败!"
		except:
			print u"授权失败!"
			raise

demo = kp_demo()
if demo.is_authorized():
	print demo.oauth_token
	print demo.oauth_token_secret
	print "已经授权!"
else:
	demo.authorized()


