import xmlrpclib
import time
from datetime import datetime, timedelta
import threading
import smtplib
import urllib
import re
import logging
import random
import csv

import ystockquote
import numpy as np
from numpy import convolve


username = 'shemer77'
password = 'boktai2'
server = xmlrpclib.Server('https://' + username + ':' + password + '@108.61.63.199:8000')

logging.basicConfig(
    filename='Strategy1.log',
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG, )


def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message, login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.ehlo()
    server.starttls()
    server.login(login, password)
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()


shares = 1
# Need to figure out time
def strategyone():
    bought_mode = False
    global server

    logging.info(
        "Strategy One:SPX OPENS MORE THAN 2% ABOVE ITS CLOSE OF 3 DAYS AGO AND IS ABOVE 200DMA. BUY ON CLOSE. SELL 6 DAYS")
    logging.info("Current price of SPX " + ystockquote.get_price("SPY"))
    #chance of working is 79%
    logging.info('\n')
    todays_date = time.strftime("%Y-%m-%d")
    logging.info("todays date is " + todays_date)

    date_N_days_ago = datetime.now() - timedelta(days=3)
    f = str(date_N_days_ago)
    date_three_days_ago = f.split(' ')[0]
    logging.info("the date three days ago is " + date_three_days_ago)

    historical_price = ystockquote.get_historical_prices("SPY", date_three_days_ago, todays_date)
    histpricelist = historical_price.items()
    histpricelist.sort()

    try:
        logging.info("the close from 3 days ago is " + historical_price[date_three_days_ago]['Close'])
        threedaysagoclose = float(historical_price[date_three_days_ago]['Close'])
    except Exception:
        logging.info("looks like the last closing day was a non trading day fixing the problem")
        logging.info("the close from the last trading day is " + str(histpricelist[0][1]['Close']))
        threedaysagoclose = float(histpricelist[0][1]['Close'])

    content = urllib.urlopen("https://www.google.com/finance?q=SPY").read()
    m = re.search('(?:snapfield="open".Open\n<\/td>\n<td class="val">)(.*)', content)
    try:
        logging.info("The open today is " + m.group(1))
        todaysopen = float(m.group(1))
    except Exception:
        logging.info(
            "You got an excpetion trying to get open today, most likely due to the fact that the market isnt open yet, waiting two hours then trying again")
        time.sleep(7200)
        logging.info("The open today is " + m.group(1))
        todaysopen = float(m.group(1))

    logging.info("the current price is this perecntage above or below its close of 3 days ago " + str(
        (float(ystockquote.get_price("SPY")) / threedaysagoclose) - 1))

    logging.info("the current 200 dma is " + str(float(ystockquote.get_200day_moving_avg("SPY"))))
    logging.info("when these show TRUE TRUE FALSE YOU SHOULD BUY")
    logging.info("todays open is 2% above its close from three days ago")
    logging.info(todaysopen >= 1.02 * threedaysagoclose)
    logging.info("Current price is above its 200 dma")
    logging.info(float(ystockquote.get_price("SPY")) > float(ystockquote.get_200day_moving_avg("SPY")))
    logging.info("bought mode is set to")
    logging.info(bought_mode)

    if todaysopen >= 1.02 * threedaysagoclose and float(ystockquote.get_price("SPY")) > float(
            ystockquote.get_200day_moving_avg("SPY")) and (bought_mode is False):
        price_I_bought_at = float(ystockquote.get_price("SPY"))
        current_money = server.current_money()
        logging.info("Current money is" + str(current_money))
        total_to_spend = (.79 / 3) * current_money
        logging.info('\n')
        logging.info("total to spend is" + str(total_to_spend))
        shares = int(ystockquote.get_price("SPY")) / int(total_to_spend)
        logging.info('\n')
        logging.info("# of shares" + int(shares))
        logging.info('\n')
        server.buy_stock("SPY", int(ystockquote.get_price("SPY")), shares)
        day_N_days_from_now = datetime.now() + timedelta(days=6)
        l = str(day_N_days_from_now)
        day_to_sell = l.split(' ')[0]
        logging.info(day_to_sell)
        bought_mode = True
        sendemail(from_addr='shemer77@gmail.com',
                  to_addr_list=['shemer77@gmail.com'],
                  cc_addr_list='',
                  subject='StrategyOne Executed',
                  message='StrategyOne has been Executed',
                  login='shemer77',
                  password='elitehacker77')

    if bought_mode is True and day_to_sell == todays_date:
        logging.info("going to sell")
        server.sell("SPY", int(ystockquote.get_price("SPY")), shares)
        bought_mode = False

    if bought_mode is True and (float(ystockquote.get_price("SPY"))) <= (price_I_bought_at * .93):
        logging.info("I hit my stop")
        server.sell("SPY", int(ystockquote.get_price("SPY")), shares)
        bought_mode = False

    threading.Timer(84600, strategyone).start()


def strategytwo():
    bought_mode = False
    global server

    logging.info(
        "Strategy TWO:SPX MAKES A NEW 50 DAY HIGH. THE % of NYSE issues making new highs falls by at least 2%. SHORT SPX on CLOSE. BUY 5 DAYS LATER")
    logging.info("Current price of SPX")
    logging.info(ystockquote.get_price("SPY"))
    #chance of working is 95%
    logging.info('\n')
    todays_date = time.strftime("%Y-%m-%d")
    logging.info("todays date is " + todays_date)
    logging.info('\n')

    date_N_days_ago = datetime.now() - timedelta(days=50)
    f = str(date_N_days_ago)
    date_fifty_days_ago = f.split(' ')[0]
    logging.info("the date 50 days ago is")
    logging.info(date_fifty_days_ago)
    logging.info('\n')

    historical_price = ystockquote.get_historical_prices("SPY", date_fifty_days_ago, todays_date)
    histpricelist = historical_price.items()
    histpricelist.sort()

    try:
        logging.info("the close from fifty days ago is " + historical_price[date_fifty_days_ago]['Close'])
        fiftydaysagoclose = float(historical_price[date_fifty_days_ago]['Close'])
        logging.info('\n')
    except Exception:
        logging.info("looks like the fifty days ago close was a non trading day fixing the problem")
        logging.info("the close from fifty days ago is " + str(histpricelist[0][1]['Close']))
        fiftydaysagoclose = float(histpricelist[0][1]['Close'])
        logging.info('\n')

    #getpercentofnysesissues making new highs


    def mainpartofthisstrategy():
        #get the price every 10 minutes and see if it matches the strategy
        current_price = float(ystockquote.get_price("SPY"))


    threading.Timer(84600, strategytwo).start()


def strategythree():
    print("shit")
    #SPX Closes down more than 1.5x yesterdays 20 DAY ATR. ToDAY IS FRIDAY. BUY ON CLOSE SELL 1 days later


def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start


current_price_array = []
portfolio = csv.reader(open("spy.csv", "rb"))
portfolio_list = []
portfolio_list.extend(portfolio)
for data in portfolio_list:
    current_price_array.append(float(data[0]))
print current_price_array

#current_price_array = [float(randrange_float(180, 186, 0.1)) for _ in range(5758)]
def fetchcurrentprice():
    content1 = urllib.urlopen("https://www.google.com/finance?q=SPY").read()
    m = re.search('(?:<span class=nwp>\n)(.*)', content1)
    print(m.group(1))
    while not 'Close' in m.group(1):
        content1 = urllib.urlopen("https://www.google.com/finance?q=SPY").read()
        m = re.search('(?:<span class=nwp>\n)(.*)', content1)
        current_price = float(ystockquote.get_price("SPY"))
        print(current_price)
        current_price_array.append(current_price)
        print(current_price_array)
        if len(current_price_array) > 5760:
            print("len of current price array was greater than 5760")
            del current_price_array[0]
        np.savetxt("spy.csv", current_price_array, fmt='%10.2f', delimiter=",")
    time.sleep(15)
    threading.Timer(30, fetchcurrentprice).start()


def movingaverage(values, window):
    weights = np.repeat(1.0, window) / window
    sma = np.convolve(values, weights, 'valid')
    return sma


best_window_size = 0
best_sell_x_ticks_later = 0


def calc_best_ma():
    global best_window_size
    global best_sell_x_ticks_later
    i = 1
    best_money_made_array = []
    arrayplus2 = current_price_array[:]
    sell_x_days_later_array = []
    while i <= 1000:
        print i
        #logging.info(i)
        current_money = 10000
        bought_state = False
        #logging.info( "My current price array is")
        #logging.info( current_price_array)
        #logging.info( "My adjsuted current price list is")
        if (i > 1):
            arrayplus2.pop(0)
        print arrayplus2
        #logging.info(arrayplus2)
        ma = movingaverage(current_price_array, i)
        # print "my moving averages are"
        #logging.info("my moving averages are")
        # logging.info(ma)
        print ma

        sell_ticks_later = 1
        best_new_money = []
        while sell_ticks_later <= 384:
            new_money = current_money
            print("sell ticks later " + str(sell_ticks_later))
            #logging.info("sell ticks later " + str(sell_ticks_later))
            index = 0
            for a, b in zip(ma, arrayplus2):
                #print("current index is " + str(index))
                if b > a and bought_state == False:
                    #print("i have bought")
                    #print(" my b is")
                    #print(b)
                    #print "my a is "
                    # print(a)
                    print("I am going to pay " + str(arrayplus2[index]))
                    #logging.info("I am going to pay " + str(arrayplus2[index]))
                    new_money -= 20 * (arrayplus2[index])
                    new_money -= 7
                    bought_state = True
                    print("I am going to sell at this many ticks later " + str(sell_ticks_later))
                    # logging.info("I am going to sell at this many ticks later " + str(sell_ticks_later))
                    #if there is a value less than 10% of my buyprince(arrayplus2[index]) within any values from arrayplus2[index] to arrayplus2[index+sell_ticks_later]) sell else
                    try:
                        print("I am going to sell at this price " + str(arrayplus2[index + sell_ticks_later]))
                        # logging.info("I am going to sell at this price " + str(arrayplus2[index + sell_ticks_later]))
                        new_money += 20 * (arrayplus2[index + sell_ticks_later])
                        new_money += 7
                    except Exception:
                        print("i cant sell this many days ahead, so im refunding the money")
                        #logging.info("i cant sell this many days ahead, so im refunding the money")
                        new_money += 20 * (arrayplus2[index])
                        new_money += 7
                    print("current money so far is " + str(new_money))
                    # logging.info("current money so far is " + str(new_money))

                index += 1
                bought_state = False
            best_new_money.append(new_money)
            sell_ticks_later += 1
        print("just finsihed iterating through all possible sell_ticks")
        #logging.info("just finsihed iterating through all possible sell_ticks")
        print(best_new_money)
        #logging.info(best_new_money)
        print("best sell x days later is at position " + str(best_new_money.index(max(best_new_money))))
        #logging.info("best sell x days later is at position " + str(best_new_money.index(max(best_new_money))))
        sell_x_days_later_array.append(int(best_new_money.index(max(best_new_money))))
        current_money = max(best_new_money)
        print "I just finished iteration"
        #logging.info("I just finished iteration")
        print(i)
        #logging.info(i)
        print"My current money is"
        #logging.info("my current money is" + str(current_money))
        print current_money
        best_money_made_array.append(current_money)
        i += 1
    print("all done")
    logging.info("all done")
    print(best_money_made_array)
    print(max(best_money_made_array))
    print("max money made is at element " + str(best_money_made_array.index(max(best_money_made_array))))
    logging.info("max money made is at element " + str(best_money_made_array.index(max(best_money_made_array))))
    print("add one to that to get the window size")
    logging.info("add one to that to get the window size")
    best_window_size = int(best_money_made_array.index(max(best_money_made_array))) + 1
    print("the number of days to sell later is " + str(
        sell_x_days_later_array[int(best_money_made_array.index(max(best_money_made_array)))]))
    logging.info("the number of days to sell later is " + str(
        sell_x_days_later_array[int(best_money_made_array.index(max(best_money_made_array)))]))
    best_sell_x_ticks_later = int(sell_x_days_later_array[int(best_money_made_array.index(max(best_money_made_array)))])
    threading.Timer(518400, calc_best_ma).start()


def strategyfour():
    print("shit")

#strategyone()
#strategytwo()
#strategythree()
#fetchcurrentprice()
#calc_best_ma()
