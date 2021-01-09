from bs4 import BeautifulSoup
import requests
import json
import telebot

bot = telebot.TeleBot("YOUR_API_KEY", parse_mode='markdown')

slug = []
name = []
symbol = []
volume = []
price = []
pchange1h = []
pchange24h = []
pchange7d = []


def getData():
    cmc = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id="__NEXT_DATA__", type="application/json")
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

    for i in listings:
        coins[str(name.append(i['name']))] = slug.append(i['slug']), \
                                             symbol.append(i['symbol']), \
                                             price.append(i['quote']['USD']['price']), \
                                             volume.append(i['quote']['USD']['volume_24h']), \
                                             pchange1h.append(i['quote']['USD']['percent_change_1h']), \
                                             pchange24h.append(i['quote']['USD']['percent_change_24h']), \
                                             pchange7d.append(i['quote']['USD']['percent_change_7d'])

@bot.message_handler(commands=['top10', 'topten'])
def send_toptenCoins(message):
    msg = message.chat.id
    bot.send_chat_action(msg, 'typing')
    getData()
    for i in range(0, 10):
        bot.send_message(msg, "============================="
                         + "\n*Name:* " + "`" + name[i] + "`"
                         + "\n*Symbol:* " + "`" + symbol[i] + "`"
                         + "\n*price:* " + "`$" + str(price[i]) + "`"
                         + "\n*24 Hour volume:* " + "`$" + str(volume[i]) + "`"
                         + "\n*1 Hour change:* " + "`" + str(pchange1h[i]) + "%`"
                         + "\n*24 Hour change:* " + "`" + str(pchange24h[i]) + "%`"
                         + "\n*Weekly change:* " + "`" + str(pchange7d[i]) + "%`"
                         + "\n=============================")

@bot.message_handler(commands=['bestperforming', 'bp'])
def send_best_performing_coin(message):
    getData()
    msg = message.chat.id
    bot.send_chat_action(msg, 'typing')
    bot.send_message(msg, "Coin name: " + name[pchange7d.index(max(pchange7d))] +
                     "\nWeekly change: %" + str(pchange7d[pchange7d.index(max(pchange7d))]) +
                     "\nCurrent price: $" + str(price[pchange7d.index(max(pchange7d))]))

@bot.message_handler(commands=['worstperforming', 'wp'])
def send_worst_performing_coin(message):
    getData()
    msg = message.chat.id
    bot.send_chat_action(msg, 'typing')
    bot.send_message(msg, "Coin name: " + name[pchange7d.index(min(pchange7d))] +
                     "\nWeekly change: %" + str(pchange7d[pchange7d.index(min(pchange7d))]) +
                     "\nCurrent price: $" + str(price[pchange7d.index(min(pchange7d))]))

@bot.message_handler(commands=['allcoins'])
def send_allCoins(message):
    coinList = []
    coinListStr = "\n"
    getData()
    msg = message.chat.id
    bot.send_chat_action(msg, 'typing')
    for i in range(len(name)):
        coinList.append(name[i] + ": " + symbol[i])
    bot.send_message(msg, "*" + coinListStr.join(coinList) + "*")

@bot.message_handler(commands=['coindata', 'cd'])
def send_coindata(message):
    msg = message.chat.id
    bot.send_chat_action(msg, 'typing')
    try:
        if len(message.text.split()) <= 1:
            bot.send_message(msg, "Enter a coin symbol.\n"
                                  "Example: \n`/coindata btc\n` or\n`/cd btc`")
        else:
            getData()
            coinrq = symbol.index(message.text.split()[1].upper())
            bot.send_message(msg, "============================="
                         + "\n*Name:* " + "`" + name[coinrq] + "`"
                         + "\n*Symbol:* " + "`" + symbol[coinrq] + "`"
                         + "\n*price:* " + "`$" + str(price[coinrq]) + "`"
                         + "\n*24 Hour volume:* " + "`$" + str(volume[coinrq]) + "`"
                         + "\n*1 Hour change:* " + "`" + str(pchange1h[coinrq]) + "%`"
                         + "\n*24 Hour change:* " + "`" + str(pchange24h[coinrq]) + "%`"
                         + "\n*Weekly change:* " + "`" + str(pchange7d[coinrq]) + "%`"
                         + "\n=============================")
    except ValueError:
        bot.send_message(msg, "Couldn't find this coin, sorry!")


bot.polling()
