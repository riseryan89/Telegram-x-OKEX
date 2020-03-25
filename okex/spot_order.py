import hmac
import base64
import requests
import json
from dbconn import dbConn

import datetime

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'
apikey = 'd885b2a7-01dd-4e24-a8f2-d4018bdb960c'
seckey = '4D79A274FA568A4610F0AF9B9B04DD7D'
passph = 'Nurzym9p54hmzHd'

base_url = 'https://okex.co.kr'


# signature
def signature(timestamp, method, request_path, body, secret_key):
	if str(body) == '{}' or str(body) == 'None':
		body = ''
	message = str(timestamp) + str.upper(method) + request_path + str(body).replace(' ', '')
	mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
	d = mac.digest()
	return base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
	header = dict()
	header[CONTENT_TYPE] = APPLICATION_JSON
	header[OK_ACCESS_KEY] = api_key
	header[OK_ACCESS_SIGN] = sign
	header[OK_ACCESS_TIMESTAMP] = str(timestamp)
	header[OK_ACCESS_PASSPHRASE] = passphrase
	return header


def get_time():
	base = 'https://okex.co.kr'
	time_request_path = '/api/general/v3/time'
	time_res = requests.get(base + time_request_path)
	timestamp = time_res.json()["epoch"]
	return timestamp


def parse_params_to_str(params):
	url = '?'
	for key, value in params.items():
		url = url + str(key) + '=' + str(value) + '&'

	return url[0:-1]


def get_sub_balance():
	try:
		base = 'https://okex.co.kr'
		batch_request_path = '/api/account/v3/wallet'

		time = get_time()
		header = get_header(apikey, signature(time, 'GET', batch_request_path, None, seckey), time, passph)

		# do request
		response = requests.get(base + batch_request_path, headers=header)
		return response.json()
	except:
		return -1


def fund_trans(amount):
	try:
		base = 'https://okex.co.kr'
		params = {'currency': 'USDT', 'amount': amount, 'from': 6, 'to': 1}
		place_request_path = '/api/account/v3/transfer' + parse_params_to_str(params)
		time = get_time()
		body = json.dumps(params)
		header = get_header(apikey, signature(time, 'POST', place_request_path, body, seckey), time, passph)
		response = requests.post(base + place_request_path, data=body, headers=header)
		return response.json()
	except:
		return -1


def batch_order(sym):
	try:
		base = 'https://okex.co.kr'
		param = {"status": 'open', "instrument_id": sym}
		batch_request_path = '/api/spot/v3/orders' + parse_params_to_str(param)

		time = get_time()
		header = get_header(apikey, signature(time, 'GET', batch_request_path, None, seckey), time, passph)

		# do request
		response = requests.get(base + batch_request_path, headers=header)
		return response.json()
	except:
		return -1

def batch_filled_order(sym):
	try:
		base = 'https://okex.co.kr'
		param = { "instrument_id": sym}
		batch_request_path = '/api/spot/v3/orders_pending' + parse_params_to_str(param)

		time = get_time()
		header = get_header(apikey, signature(time, 'GET', batch_request_path, None, seckey), time, passph)

		# do request
		response = requests.get(base + batch_request_path, headers=header)
		return response.json()
	except:
		return -1

def place_order(otype, side, instrument_id, size, margin_trading=1,  price='', order_type='0'):
	base = 'https://okex.co.kr'
	params = {'type': otype, 'side': side, 'instrument_id': instrument_id, 'size': size,
	          'price': price, 'margin_trading': margin_trading, 'order_type': order_type}
	place_request_path = '/api/spot/v3/orders' + parse_params_to_str(params)
	time = get_time()
	body = json.dumps(params)
	header = get_header(apikey, signature(time, 'POST', place_request_path, body, seckey), time, passph)
	response = requests.post(base + place_request_path, data=body, headers=header)
	return response.json()


def delete_order(sym, order_id):
	base = 'https://okex.co.kr'
	params = { "instrument_id": sym }
	place_request_path = '/api/spot/v3/cancel_orders/' + order_id
	time = get_time()
	body = json.dumps(params)
	header = get_header(apikey, signature(time, 'POST', place_request_path, body, seckey), time, passph)
	response = requests.post(base + place_request_path, data=body, headers=header)
	print(order_id)
	print(response.json())
	return response.json()



# place_order(otype='limit', side='sell', instrument_id='USDT-KRW', price='1180', size='1')
# request example
# set the request url

# class AsyncTasks:
# 	def __init__(self):
# 		pass
#
# 	def order_list(self):

# db = dbConn().connect()
#
# try:
# 	with db.cursor() as cursor:
# 		orderlist = batch_order()
# 		if orderlist != -1:
# 		# Create a new record
# 			for i in orderlist:
# 				sql = "INSERT INTO `app_bot_order_list` (`order_id`, `client_oid`, `filled_notional`, `filled_size`, `instrument_id`, \
# 				       `price`, `size`, `side`, `state`, `status`, `type`, `datetime_created`)  \
# 			           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `filled_notional`=%s, `filled_size`=%s, \
# 				       `state`=%s, `status`=%s"
# 				cursor.execute(sql, (i['order_id'], i['client_oid'], i['filled_notional'], i['filled_size'],
# 				                     i['instrument_id'], i['price'], i['size'], i['side'],
# 				                     i['state'], i['status'], i['type'], i['created_at'],
# 				                     i['filled_notional'], i['filled_size'], i['state'], i['status']))
# 			db.commit()
# 		else:
# 			print("error")
# except:
# 	pass
# finally:
# 	db.close()