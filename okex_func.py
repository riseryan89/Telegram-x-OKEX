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
apikey = 'api-key'
seckey = 'sec-key'
passph = 'ex-pass'

base_url = 'https://okex.co.kr'


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


def get_topup_addr():
    try:
        base = 'https://okex.co.kr'
        param = {"currency": 'USDT'}
        batch_request_path = '/api/account/v3/deposit/address' + parse_params_to_str(param)

        time = get_time()
        header = get_header(apikey, signature(time, 'GET', batch_request_path, None, seckey), time, passph)

        # do request
        response = requests.get(base + batch_request_path, headers=header)
        return response.json()
    except:
        return -1


def get_balance():
    try:
        base = 'https://okex.co.kr'
        batch_request_path = '/api/spot/v3/accounts'

        time = get_time()
        header = get_header(apikey, signature(time, 'GET', batch_request_path, None, seckey), time, passph)

        # do request
        response = requests.get(base + batch_request_path, headers=header)

        res = '코인 : 총 잔고(사용가능)\n'
        for re in response.json():
            res = res + "{} : {} ({}) \n".format(re['currency'], re['balance'], re['available'])
        return res
    except:
        return -1