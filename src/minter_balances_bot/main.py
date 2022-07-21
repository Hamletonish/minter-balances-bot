import config
from telebot import TeleBot, types
from api_requests import MinterApi, ExchangeRate

bot = TeleBot(config.bot_token)

markup = types.ReplyKeyboardMarkup()
markup.row('/btc', '/bip')

# action when starting or receiving any text message
@bot.message_handler(commands=["start"])
def repeat_start_message(message):
    bot.send_message(message.chat.id, 'Choose your button', reply_markup=markup)

# action when receiving command "/btc"
@bot.message_handler(commands=["btc"])
def get_btc_price(message):
    bot.send_message(message.chat.id, ExchangeRate().get_binance_rate('BTCUSDT'), reply_markup=markup)

# action when receiving command "/bip"
@bot.message_handler(commands=["bip"])
def get_balances(message):
    msg_text = ''
    try:
        # getting and calculating the required values and formatting the text message
        price = ExchangeRate().get_bithumb_rate('BIP-USDT')
        msg_text += f'Current BIP price: *{price}*\n=============================\n'
        total = 0
        for i, wallet in enumerate(config.wallets):
            wallet_delegations = MinterApi().get_delegations(wallet)
            wallet_balance     = MinterApi().get_current_balance(wallet)
            wallet_unbonds     = MinterApi().get_unbonds(wallet)
            wallet_total       = wallet_delegations + wallet_balance + wallet_unbonds
            total    += wallet_total
            msg_text += f'*Wallet {i+1}*\nDelegations: {wallet_delegations}\nBalance: {wallet_balance}\nUnbonds: {wallet_unbonds}\n*Total:* {wallet_total}\n=============================\n'
        msg_text += f'Total BIP: {round(total,2)}\nTotal USD: {round(total*price, 2)}'
        # sending the message
        bot.send_message(message.chat.id, msg_text, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, 'Some error happened!', reply_markup=markup)

if __name__ == '__main__':
     bot.infinity_polling()