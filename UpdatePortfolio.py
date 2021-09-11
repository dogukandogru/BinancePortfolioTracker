from openpyxl import load_workbook
from binance import Client
import json

def getTotalPurchased(client, coin):
    trades = client.get_my_trades(symbol=coin)
    totalPaid = 0
    for trade in trades:
        if trade['isBuyer']:
            totalPaid += float(trade['quoteQty'])
        else:
            totalPaid -= float(trade['quoteQty'])
    
    return totalPaid

def getTotalBalance(balances, prices):
    totalBalance = 0
    for balance in balances:
        if float(balance['free']) + float(balance['locked']) > 0:
            if balance['asset'] == 'USDT':
                totalBalance += float(balance['free']) + float(balance['locked'])
            else:
                totalBalance += (float(balance['free']) + float(balance['locked'])) * getPrice(prices, balance['asset'] + 'USDT')
    return totalBalance

def getAccountCoins(balances):
    coins = []
    for balance in balances:
        
        if float(balance['free']) + float(balance['locked']) > 0 and balance['asset'] != 'USDT':
            if (float(balance['free']) + float(balance['locked'])) * float(client.get_avg_price(symbol=balance['asset'] + 'USDT')['price']) > 10:
                coins.append(balance['asset'] + "USDT")
    return coins

def getPrice(prices, ticker):
    for price in prices:
        if price['symbol'] == ticker:
            return float(price['price'])

def getAmount(balances, ticker):
    ticker = ticker[:ticker.index('USDT')]
    for balance in balances:
        if balance['asset'] == ticker:
            return float(balance['free'])


apiKeyFile = open('API_KEYS.json')
apiData = json.load(apiKeyFile)
apiKeyFile.close()

API_KEY = apiData['API_KEY']
SECRET_KEY = apiData['SECRET_KEY']

if API_KEY == '' or SECRET_KEY == '':
    print('API_KEY or SECRET_KEY not found in API_KEYS.json')
    exit()

client = Client(API_KEY, SECRET_KEY)
balances = client.get_account()['balances']
prices = client.get_all_tickers()
coins = getAccountCoins(balances)

totalBalance = getTotalBalance(balances, prices)


workbook = load_workbook(filename="Portfolio.xlsx")
sheet = workbook.active
sheet["L8"].value = totalBalance

for i in range (2,len(coins)+2):
    ticker = coins[i-2]
    sheet["A"+str(i)] = ticker
    price = getPrice(prices, ticker)
    amount = getAmount(balances, ticker)
    totalPurchased = getTotalPurchased(client, ticker)
    if sheet["D"+str(i)].value == None:
        sheet["D"+str(i)].value = totalPurchased
    sheet["B"+str(i)].value = price
    sheet["C"+str(i)].value = amount
    sheet["E"+str(i)].value = "=D{0} / C{1}".format(str(i), str(i))
    sheet["F"+str(i)].value = "=B{0} * C{1}".format(str(i), str(i))
    sheet["G"+str(i)].value = "=F{0} - D{1}".format(str(i), str(i))
    sheet["H"+str(i)].value = "=((B{0} - E{1}) / E{2})".format(str(i), str(i), str(i))
    sheet["J"+str(i)].value = "=I{0} * C{1}".format(str(i), str(i))
    sheet["K"+str(i)].value = "=J{0} - D{1}".format(str(i), str(i))
    






workbook.save(filename="Portfolio.xlsx")
