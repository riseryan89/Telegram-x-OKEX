import okex.account_api as account
import okex.spot_api as spot
import threading
from dbconn import op_updater, orderbook_updater
import requests
from okex.spot_order import place_order, batch_order, delete_order
import json
import random


class AsyncTasks:
	def __init__(self):
		pass

	def stat_updater(self):
		try:
			accountAPI = account.AccountAPI(api_key, seceret_key, passphrase, True)
			result = accountAPI.get_top_up_address('USDT')
			for addr in result:
				if addr['currency'] == 'usdt-erc20' or addr['currency'] == 'usdt-trc20':
					op_updater(addr['currency'], addr['address'])
		except Exception as e:
			print(e)
			pass
		threading.Timer(300, self.stat_updater).start()

	def orderbook_usdtkrw(self):
		req = requests.get('https://www.okex.co.kr'+ '/api/spot/v3/instruments/USDT-KRW/book')
		return req.json()

	def order_placer(self):
		try:
			orderbook = self.orderbook_usdtkrw()
			batch = batch_order()

			best_bid_price = float(orderbook['bids'][0][0])
			best_bid_qty = orderbook['bids'][0][1]
			best_ask_price = float(orderbook['asks'][0][0])
			second_best_bid_price = float(orderbook['bids'][1][0])
			second_best_ask_price = float(orderbook['asks'][1][0])
			best_ask_qty = orderbook['asks'][0][1]
			spread = float(orderbook['asks'][0][0]) - float(orderbook['bids'][0][0])
			max_spread = 2.2

			if len(batch) > 0:
				for b in batch:
					order_price = float(b['price'])
					delete_order(b['order_id'])
			# 		if b['side'] == 'buy':
			# 			if len(batch) == 1 and spread >= max_spread:
			# 				place_order(otype='limit', side='sell', instrument_id='USDT-KRW', size='2', price=str(best_ask_price - 0.1))
			# 			if best_bid_price == order_price and b['size'] == best_bid_qty:
			#
			# 				if round(second_best_bid_price + 0.1, 1) < round(order_price, 1):
			# 					delete_order(b['order_id'])
			# 					if spread >= max_spread:
			# 						place_order(otype='limit', side='buy', instrument_id='USDT-KRW', size='2', price=str(round(second_best_bid_price + 0.1, 1)))
			# 				else:
			# 					print("Buy PASSED")
			# 			else:
			# 				delete_order(b['order_id'])
			# 				if spread >= max_spread:
			# 					print(str(best_bid_price + 0.1))
			# 					place_order(otype='limit', side='buy', instrument_id='USDT-KRW', size='2', price=str(round(best_bid_price + 0.1, 1)))
			#
			# 		elif b['side'] == 'sell':
			# 			if len(batch) == 1 and spread >= max_spread:
			# 				place_order(otype='limit', side='buy', instrument_id='USDT-KRW', size='2', price=str(round(best_bid_price + 0.1, 1)))
			#
			# 			if best_ask_price == order_price and b['size'] == best_ask_qty:
			# 				if round(second_best_ask_price - 0.1, 1) > round(order_price, 1):
			# 					delete_order(b['order_id'])
			# 					if spread >= max_spread:
			# 						place_order(otype='limit', side='sell', instrument_id='USDT-KRW', size='2', price=str(second_best_ask_price - 0.1))
			# 				else:
			# 					print("Sell PASSED")
			# 			else:
			# 				delete_order(b['order_id'])
			# 				if spread >= max_spread:
			# 					place_order(otype='limit', side='sell', instrument_id='USDT-KRW', size='2', price=str(best_ask_price - 0.1))
			# else:
			# 	if spread >= max_spread:
			# 		a = place_order(otype='limit', side='buy', instrument_id='USDT-KRW', size='2', price=str(best_bid_price + 0.1))
			#
			# 		if not a['result']:
			# 			place_order(otype='limit', side='sell', instrument_id='USDT-KRW', size='2', price=str(best_ask_price - 0.1))

		except Exception as e:
			print(e)


		threading.Timer(0.6, self.order_placer).start()

def main():
	at = AsyncTasks()
	at.stat_updater()
	at.order_placer()
	# at.orderbook_usdtkrw()


if __name__ == '__main__':
	api_key = 'd885b2a7-01dd-4e24-a8f2-d4018bdb960c'
	seceret_key = '4D79A274FA568A4610F0AF9B9B04DD7D'
	passphrase = 'Nurzym9p54hmzHd'
	main()


	# account api test
	# param use_server_time's value is False if is True will use server timestamp


