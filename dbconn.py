import pymysql.cursors
from datetime import datetime, timedelta


# Connect to the database


class dbConn():

	def __init__(self):
		pass

	def connect(self):
		connection = pymysql.connect(host='localhost',
		                             user='web',
		                             password='1234',
		                             db='dbname',
		                             port=3306,
		                             charset='utf8mb4',
		                             cursorclass=pymysql.cursors.DictCursor)
		return connection


def update_op(key: object, value: object) -> object:
	connection = dbConn().connect()
	try:
		with connection.cursor() as cursor:
			# Create a new record
			sql = "UPDATE `app_op_context` SET `op_value`=%s, `data_lastupdated_on`=%s WHERE `op_key`= %s"
			cursor.execute(sql, (value, datetime.now(), key))

		# connection is not autocommit by default. So you must commit to save
		# your changes.
		connection.commit()
		connection.close()
		return True

	except Exception as e:
		print(e)
		return False


def get_op(key):
	connection = dbConn().connect()
	try:
		with connection.cursor() as cursor:
			# Create a new record
			sql = "SELECT * FROM `app_op_context` WHERE `op_key`= %s"
			cursor.execute(sql, (key))
			row = cursor.fetchone()

		connection.close()
		return row

	except Exception as e:
		print(e)
		return False


def logger(type, bot_id, log):
	db = dbConn().connect()
	try:
		with db.cursor() as cursor:
			# Create a new record
			sql = "INSERT INTO `app_bot_logs` (`logs`, `datetime_created`, `bot_index_id`, `type`)  \
	               VALUES (%s, %s, (SELECT `no` FROM `app_bot_type` WHERE `no` = %s), %s)"
			cursor.execute(sql, (log, datetime.now(), bot_id, type))
		db.commit()
	except:
		try:
			with db.cursor() as cursor:
				# Create a new record
				sql = "SELECT `bot_name`, `bot_nickname` FROM `app_bot_log` WHERE `no`=%s"
				cursor.execute(sql, (bot_id))
				result = cursor.fetchone()
				logger_sql = "INSERT INTO `app_bot_log` (`logs`, `datetime_created`, `bot_index_id`, `type`)  \
	               VALUES (%s, %s, (SELECT `no` FROM `app_bot_type` WHERE `no` = %s), %s)"
				error_log = result['bot_name'] + " LOG SYSTEM ERROR."
			cursor.execute(logger_sql, (error_log, datetime.now(), bot_id, type))
		except:
			print("DATABASE SERVER DOWN")

	finally:
		db.close()


def orderbook_updater(book):
	asks = book['asks']
	bids = book['bids']
	connection = dbConn().connect()
	quote_c = "KRW"
	base_c = "USD"
	try:
		with connection.cursor() as cursor:
			# Create a new record
			sql = "UPDATE `app_bot_order_book` SET `price` = (CASE `order`  \
		           WHEN 'bid-1' THEN %s WHEN 'bid-2' THEN %s WHEN 'bid-3' THEN %s WHEN 'bid-4' THEN %s WHEN 'bid-5' THEN %s \
		           WHEN 'ask-1' THEN %s WHEN 'ask-2' THEN %s WHEN 'ask-3' THEN %s WHEN 'ask-4' THEN %s WHEN 'ask-5' THEN %s END) \
		           , `qty` = (CASE `order` \
		           WHEN 'bid-1' THEN %s WHEN 'bid-2' THEN %s WHEN 'bid-3' THEN %s WHEN 'bid-4' THEN %s WHEN 'bid-5' THEN %s \
		           WHEN 'ask-1' THEN %s WHEN 'ask-2' THEN %s WHEN 'ask-3' THEN %s WHEN 'ask-4' THEN %s WHEN 'ask-5' THEN %s END) \
		           , `num_order` = (CASE `order` \
		           WHEN 'bid-1' THEN %s WHEN 'bid-2' THEN %s WHEN 'bid-3' THEN %s WHEN 'bid-4' THEN %s WHEN 'bid-5' THEN %s \
		           WHEN 'ask-1' THEN %s WHEN 'ask-2' THEN %s WHEN 'ask-3' THEN %s WHEN 'ask-4' THEN %s WHEN 'ask-5' THEN %s END) \
		           WHERE `symbol`='USDTKRW'"
			cursor.execute(sql, (bids[0][0], bids[1][0], bids[2][0], bids[3][0], bids[4][0], asks[0][0], asks[1][0], asks[2][0], asks[3][0], asks[4][0],
			                     bids[0][1], bids[1][1], bids[2][1], bids[3][1], bids[4][1], asks[0][1], asks[1][1], asks[2][1], asks[3][1], asks[4][1],
			                     bids[0][2], bids[1][2], bids[2][2], bids[3][2], bids[4][2], asks[0][2], asks[1][2], asks[2][2], asks[3][2], asks[4][2]))
			connection.commit()
	except Exception as e:
		print(e)
		logger(1, 2, "[ERROR] OKEX USDT/KRW ORDERBOOK UPDATE ERROR " + quote_c + base_c)

	try:
		with connection.cursor() as cursor:
			# Create a new record
			sql = "SELECT `datetime_created` FROM `app_bot_logs` WHERE `bot_index_id`=2 ORDER BY `datetime_created` DESC"
			cursor.execute(sql)
			result = cursor.fetchone()
			if result["datetime_created"] < datetime.now() - timedelta(minutes=5):
				logger(9, 2, "[OK] OKEX USDT/KRW ORDERBOOK UPDATED " + quote_c + base_c)
	except Exception as e:
		print(e)
