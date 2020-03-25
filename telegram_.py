# from telegram.ext import Updater, CommandHandler
# import okex_func as okex
# from dbconn import get_op, update_op
#
#
# def help(update, context):
#     old_get_up = get_op('bot_status')
#
#     update.message.reply_text('현재 봇 상태 : {} \n'.format(old_get_up['op_value']) +
#                               '\n'
#                               '1. /help   => 커맨드 리스트\n'
#                               '2. /deposit_addr   => 테더 입금주소(OKEX)\n'
#                               '3. /balance    => 잔고 확인\n'
#                               '4. /target_krw xxxx  => 목표 KRW 액수설정 xxxx원\n'
#                               '5. /bot_stop    => 봇 정지\n'
#                               '6. /bot_start    => 봇 시작')
#
# def deposit_addr(update, context):
#     res = okex.get_topup_addr()
#     if res == -1:
#         update.message.reply_text('짧은시간 많은 요청이 있었거나 네트워크 상태가 원활하지 않습니다. 잠시후 다시 이용해 주세요.')
#     else:
#         trc20 = ''
#         erc20 = ''
#         for addr in res:
#             if addr['currency'] == 'usdt-trc20':
#                 trc20 = addr['address']
#             elif addr['currency'] == 'usdt-erc20':
#                 erc20 = addr['address']
#         if trc20 == '':
#             trc20 = '현재 입금 불가'
#         if erc20 == '':
#             erc20 = '현재 입금 불가'
#
#         update.message.reply_text(
#             'USDT-ERC20 : '+erc20 +'\n'
#             'USDT-TRC20 : ' + trc20
#         )
#
#
# def balance(update, context):
#     res = okex.get_balance()
#     if res == -1:
#         update.message.reply_text('짧은시간 많은 요청이 있었거나 네트워크 상태가 원활하지 않습니다. 잠시후 다시 이용해 주세요.')
#     else:
#         update.message.reply_text(res)
#
#
# def target_krw(update, context):
#     text = update['message']['text']
#     update.message.reply_text('잠시 기다리세요 처리중입니다.')
#     try:
#         text = text.split('target_krw ')[1]
#         if '@' in text:
#             text = text.split('@')[0]
#         text = text.strip()
#         res = okex.get_balance()
#         if res == -1:
#             update.message.reply_text('짧은시간 많은 요청이 있었거나 네트워크 상태가 원활하지 않습니다. 잠시후 다시 이용해 주세요.')
#         else:
#             old_get_up = get_op('target_krw')
#             update_op('target_krw', text)
#             update.message.reply_text("KRW가 {}에 도달하면, 거래가 중단됩니다. (기존 목표액: {})".format(text, old_get_up['op_value']))
#     except Exception as e:
#         print(e)
#         update.message.reply_text('/target_krw 1000 과 같이 입력하세요. KRW가 1000이상이면 더이상 거래하지 않습니다.')
#
#
# def bot_stop(update, context):
#     try:
#         old_get_up = get_op('bot_status')
#         if old_get_up['op_value'] == '중지됨':
#             update.message.reply_text('현재 봇은 가동 중이 아닙니다.')
#         else:
#             update_op('bot_status', '중지됨')
#             update.message.reply_text('봇 가동이 중지 되었습니다.')
#
#     except Exception as e:
#         print(e)
#         update.message.reply_text('짧은시간 많은 요청이 있었거나 네트워크 상태가 원활하지 않습니다. 잠시후 다시 이용해 주세요.')
#
#
# def bot_start(update, context):
#     try:
#         old_get_up = get_op('bot_status')
#         if old_get_up['op_value'] == '거래중':
#             update.message.reply_text('이미 거래 중입니다..')
#         else:
#             update_op('bot_status', '거래중')
#             update.message.reply_text('봇이 거래를 시작합니다..')
#
#     except Exception as e:
#         print(e)
#         update.message.reply_text('짧은시간 많은 요청이 있었거나 네트워크 상태가 원활하지 않습니다. 잠시후 다시 이용해 주세요.')
#
#
# if __name__ == '__main__':
#
#     api_key = 'YOUR OKEX API'
#     seceret_key = 'YOUR OKEX Secret API'
#     passphrase = 'YOUR OKEX PASS'
#     updater = Updater('TELE-TOKEN', use_context=True)
#
#     updater.dispatcher.add_handler(CommandHandler('help', help, allow_edited=False))
#     updater.dispatcher.add_handler(CommandHandler('deposit_addr', deposit_addr, allow_edited=False))
#     updater.dispatcher.add_handler(CommandHandler('balance', balance, allow_edited=False))
#     updater.dispatcher.add_handler(CommandHandler('target_krw', target_krw, allow_edited=False))
#     updater.dispatcher.add_handler(CommandHandler('bot_stop', bot_stop))
#     updater.dispatcher.add_handler(CommandHandler('bot_start', bot_start))
#     updater.start_polling()
#     updater.idle()
#
