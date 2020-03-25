import okex.account_api as account
import okex.spot_api as spot
import threading
import requests
from okex.spot_order import place_order, batch_order, delete_order, batch_filled_order, get_sub_balance, fund_trans
from dbconn import get_op, update_op
import json
import random


max_spread = 0.001
USDTKRW_order_qty = str(random.randint(99, 200))
USDTKRW_symbol = 'USDT-KRW'
USDTKRW_min_step = 0.1


class AsyncTasks:
	def __init__(self):
		pass

	def account_info(self):
		spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
		result = spotAPI.get_account_info()
		balance = {
			"btc": '',
			'eth': '',
			'usdt': '',
			'krw': ''
		}
		for coin in result:
			if coin['currency'] == 'BTC':
				balance['btc'] = coin["balance"]
			elif coin['currency'] == 'ETH':
				balance['eth'] = coin["balance"]
			elif coin['currency'] == 'USDT':
				balance['usdt'] = coin["balance"]
			elif coin['currency'] == 'KRW':
				balance['krw'] = coin["balance"]
		return balance

	def orderbook(self, pair):
		req = requests.get('https://www.okex.co.kr'+ '/api/spot/v3/instruments/'+pair+'/book')
		return req.json()

	def order_placer_USDT_KRW(self, sym, qty, step):

		try:
			balance = self.account_info()['usdt']

			orderbook = self.orderbook(sym)
			batch = batch_order(sym)
			filled_batch = batch_filled_order(sym)
			best_bid_price = float(orderbook['bids'][0][0])
			best_bid_qty = orderbook['bids'][0][1]
			best_ask_price = float(orderbook['asks'][0][0])
			second_best_bid_price = float(orderbook['bids'][1][0])
			second_best_ask_price = float(orderbook['asks'][1][0])
			best_ask_qty = orderbook['asks'][0][1]
			spread = float(orderbook['asks'][0][0]) / float(orderbook['bids'][0][0]) - 1
			old_get_up = get_op('bot_status')
			max_balance = get_op('target_krw')
			if spread < max_spread:
				print("SPREAD ISSUES ||", sym)

			if float(balance) >= float(max_balance['op_value']):
				update_op('bot_status', '중지됨')

			if len(filled_batch) > 1:
				for b in filled_batch:
					if float(b['filled_size']) > 0:
						delete_order(sym, b['order_id'])

			elif len(batch) > 0:
				for b in batch:
					print(old_get_up['op_value'])
					if old_get_up['op_value'] == '중지됨':
						delete_order(sym, b['order_id'])
					else:
						order_price = float(b['price'])
						if b['side'] == 'buy':
							delete_order(sym, b['order_id'])

						elif b['side'] == 'sell':
							if best_ask_price == order_price and b['size'] == best_ask_qty:
								if round(second_best_ask_price - step, 1) > round(order_price, 1):
									delete_order(sym, b['order_id'])
									if spread >= max_spread:
										place_order(otype='limit', side='sell', instrument_id=sym, size=qty, price=str(second_best_ask_price - step))
								else:
									print("Sell PASSED ||", sym)
							else:
								delete_order(sym, b['order_id'])
								if spread >= max_spread:
									place_order(otype='limit', side='sell', instrument_id=sym, size=qty, price=str(best_ask_price - step))
			else:
				if old_get_up['op_value'] == '중지됨':
					pass
				elif spread >= max_spread:
					place_order(otype='limit', side='sell', instrument_id=sym, size=qty, price=str(best_ask_price - step))

		except Exception as e:
			print(e)

		threading.Timer(0.6, self.order_placer_USDT_KRW, [sym, qty, step]).start()

	def get_sub(self):
		old_get_up = get_op('bot_status')
		try:
			if old_get_up['op_value'] == '중지됨':
				pass
			else:
				bals = get_sub_balance()
				if bals != -1:
					for bal in bals:
						if bal['currency'] == 'USDT' and float(bal['available']) >= 1:
							fund_trans(bal['available'])
				else:
					print('GetBalanceError')
		except Exception as e:
			print(e)

		threading.Timer(10, self.get_sub).start()

def main():
	at = AsyncTasks()
	at.order_placer_USDT_KRW(USDTKRW_symbol, USDTKRW_order_qty, USDTKRW_min_step)
	at.get_sub()


if __name__ == '__main__':
	api_key = 'd885b2a7-01dd-4e24-a8f2-d4018bdb960c'  # RyanArbi
	seceret_key = '4D79A274FA568A4610F0AF9B9B04DD7D'
	passphrase = 'Nurzym9p54hmzHd'
	main()


	# account api test
	# param use_server_time's value is False if is True will use server timestamp


