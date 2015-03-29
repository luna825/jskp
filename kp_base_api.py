# coding=utf-8
import time,math,urllib,hmac,hashlib,binascii,json,re,urllib2,cookielib

'''一些基础的接口实现'''
count = 0
def get_oauth_nonce():
	'''
	生成oauth_nonce
	'''
	global count
	count += 1
	return str(time.time()/2).replace(".","")

def get_timestamp():
	'''
	生成oauth_timestamp
	'''
	return int(math.ceil(time.time()))

def get_base_string(base_url,param_dic,method="GET"):
	'''
	生成signature需要的base_string
	'''
	l = [urllib.quote_plus(k)+"="+urllib.quote_plus(v) for k,v in param_dic.iteritems()]
	l.sort()
	return method + '&' + urllib.quote_plus(base_url)+'&'+urllib.quote_plus('&'.join(l))
def get_signature(base_string,consumer_secret_and_oauth_token):
	binary_sig = hmac.new(consumer_secret_and_oauth_token,base_string,hashlib.sha1)
	return binascii.b2a_base64(binary_sig.digest())[:-1]

def build_base_param(consumer_key):
	'''
	生成一些基础的参数。每次请求这需要用这些参数
	'''
	dic={}
	dic["oauth_nonce"] = get_oauth_nonce()
	dic["oauth_timestamp"]= str(get_timestamp())
	dic["oauth_consumer_key"]=consumer_key
	dic["oauth_signature_method"]="HMAC-SHA1"
	dic["oauth_version"]="1.0"
	return dic

def build_request_url(consumer_key,consumer_secret,base_url,oauth_token="",
	oauth_token_secret="",extra_params={},method="GET"):
	dic = build_base_param(consumer_key)
	if len(oauth_token)!=0:
		dic["oauth_token"]=oauth_token
	dic.update(extra_params)
	signature = get_signature(get_base_string(base_url,dic,method),
		consumer_secret+"&"+oauth_token_secret)
	dic["oauth_signature"]=signature
	url = base_url + "?" + urllib.urlencode(dic)
	return url

def request_token(consumer_key,consumer_secret):
	url = build_request_url(consumer_key,consumer_secret,
		"https://openapi.kuaipan.cn/open/requestToken")
	json_text = urllib.urlopen(url).read()
	j = json.loads(json_text)
	oauth_token = j["oauth_token"].encode("ascii")
	oauth_token_secret = j["oauth_token_secret"].encode("ascii")
	return (oauth_token,oauth_token_secret)

def get_authorize_url(oauth_token):
	return "https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token=%s"\
	% oauth_token

def request_access_token(consumer_key,consumer_secret,oauth_token,oauth_token_secret):
    url = build_request_url( consumer_key, consumer_secret,
                             "https://openapi.kuaipan.cn/open/accessToken",
                              oauth_token, oauth_token_secret )
    json_text = urllib.urlopen(url).read()
    j = json.loads(json_text)
    return ( j["oauth_token_secret"].encode("ascii"), j["oauth_token"].encode("ascii"), 
             j["user_id"], j["charged_dir"].encode("ascii") )

def get_account_info(consumer_key,consumer_secret,oauth_token,oauth_token_secret):
	url = build_request_url(consumer_key,consumer_secret,
		"http://openapi.kuaipan.cn/1/account_info",oauth_token,oauth_token_secret)
	json_text = urllib.urlopen(url).read()
	return json_text

def get_metadata(consumer_key,consumer_secret,oauth_token,oauth_token_secret,root,path):
	if len(path)>0 and (path[0]=='\\' or path =='/'):
		path = path[1:]
	url = build_request_url(consumer_key,consumer_secret,
		"http://openapi.kuaipan.cn/1/metadata/%s/%s" % (root,path),
		oauth_token,oauth_token_secret)
	json_text = urllib.urlopen(url).read()
	return json_text