#!/usr/bin/python
# -*- coding: cp1252 -*-

from decimal import *
from math import ceil
import threading
import time
import logging
import logging.handlers
import sys
import smtplib
import random

import btceapi


# linux version
key_file = 'btce.txt'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='btcetrading.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
#console = logging.StreamHandler()
#console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
#console.setFormatter(formatter)
# add the handler to the root logger
#logging.getLogger('').addHandler(console)

# Now, we can log to the root logger, or any other logger. First the root...

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('strat1.log')
logger1.addHandler(logging.FileHandler('strat1.log'))

loggerstrat2 = logging.getLogger('strattwo.log')
loggerstrat2.addHandler(logging.FileHandler('strattwo.log'))

loggerstrat9 = logging.getLogger('stratnine.log')
loggerstrat9.addHandler(logging.FileHandler('stratnine.log'))


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


def calculate_fee(amount):
    fee = amount * 0.002
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        fee = 0.0001
    return fee


def get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4):
    pair1 = str(pair1)
    pair2 = str(pair2)
    pair3 = str(pair3)
    pair4 = str(pair4)
    starting_money = current_usd
    #print("#LAPL = Lowest ask price of "+pair1)
    LAPL = float(eval(pair1 + 'asks[0][0]'))
    #print(LAPL)
    #print("#VL = Amount of "+pair1+" I can buy at that price")
    VL = float(eval(pair1 + 'asks[0][1]'))
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPL * VL > starting_money:
        #print("I dont have enough money to buy it all so setting it to max")
        #starting money is less then the amount I can buy; setting VL to all of my starting money
        VL = starting_money / LAPL
    #print(VL)
    #print("#VB = Amount of " + pair2 + " I can sell when buying @ that price")
    VB = float(eval(pair2 + 'bids[0][1]'))
    #print(VB)
    #print("#VN = Amount of " + pair3 + " I can buy  @ that price")
    VN = float(eval(pair3 + 'asks[0][1]'))
    #print(VN)
    #print("amount of " + pair3[:3] + " in " + pair1[:3] + " format")
    VN = return_equivalent(pair3[:3].upper(), VN, pair1[:3].upper())
    #print(VN)
    #print("#VU = Amount of " + pair4 + " I CAN SELl at that price")
    VU = float(eval(pair4 + 'bids[0][1]'))
    #print(VU)
    VU = return_equivalent(pair4[:3].upper(), VU, pair1[:3].upper())
    #print("#VU = Amount of " + pair4[:3] + " in " + pair1[:3] + " format")
    #print(VU)
    maxv = min(VL, VB, VU, VN)
    maxv = float(maxv)
    print("MY maxv that I can use is %s" % str(maxv))
    return maxv


def get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5):
    pair1 = str(pair1)
    pair2 = str(pair2)
    pair3 = str(pair3)
    pair4 = str(pair4)
    pair5 = str(pair5)
    starting_money = current_usd
    #print("#LAPL = Lowest ask price of "+pair1)
    LAPL = float(eval(pair1 + 'asks[0][0]'))
    #print(LAPL)
    #print("#VL = Amount of "+pair1+" I can buy at that price")
    VL = float(eval(pair1 + 'asks[0][1]'))
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPL * VL > starting_money:
        #print("I dont have enough money to buy it all so setting it to max")
        #starting money is less then the amount I can buy; setting VL to all of my starting money
        VL = starting_money / LAPL
    #print(VL)
    #print("#VB = Amount of " + pair2 + " I can sell when buying @ that price")
    VB = float(eval(pair2 + 'bids[0][1]'))
    #print(VB)
    #print("#VN = Amount of " + pair3 + " I can buy  @ that price")
    VN = float(eval(pair3 + 'asks[0][1]'))
    #print(VN)
    #print("amount of " + pair3[:3] + " in " + pair1[:3] + " format")
    VN = return_equivalent(pair3[:3].upper(), VN, pair1[:3].upper())
    #print(VN)
    #print("#VG = Amount of " + pair4 + " I can buy  @ that price")
    VG = float(eval(pair4 + 'asks[0][1]'))
    #print(VG)
    #print("amount of " + pair4[:3] + " in " + pair1[:3] + " format")
    VG = return_equivalent(pair4[:3].upper(), VG, pair1[:3].upper())
    #print(VG)
    #print("#VU = Amount of " + pair5 + " I CAN SELl at that price")
    VU = float(eval(pair5 + 'bids[0][1]'))
    #print(VU)
    VU = return_equivalent(pair5[:3].upper(), VU, pair1[:3].upper())
    #print("#VU = Amount of " + pair5[:3] + " in " + pair1[:3] + " format")
    #print(VU)
    maxv = min(VL, VB, VU, VN, VG)
    maxv = float(maxv)
    print("MY maxv that I can use is %s" % str(maxv))
    return maxv


def return_equivalent(currency, amount, output):
    if currency == 'USD':
        if output == 'BTC':
            return amount / float(btcusdasks[0][0])
        if output == 'LTC':
            return amount / ltcusdasks[0][0]
        if output == 'NMC':
            return amount / nmcusdasks[0][0]
        if output == 'NVC':
            return amount / nvcusdasks[0][0]
        if output == 'EUR':
            return amount / eurusdasks[0][0]
        if output == 'PPC':
            return amount / ppcusdasks[0][0]
    if currency == 'BTC':
        if output == 'USD':
            return amount * float(btcusdbids[0][0])
        if output == 'LTC':
            return amount / float(ltcbtcasks[0][0])
        if output == 'NMC':
            return amount / nmcbtcasks[0][0]
        if output == 'NVC':
            return amount / float(nvcbtcasks[0][0])
        if output == 'EUR':
            return amount * float(btceurbids[0][0])
        if output == 'PPC':
            return amount / float(ppcbtcasks[0][0])
        if output == 'RUR':
            return amount * float(btcrurbids[0][0])
    if currency == 'RUR':
        if output == 'BTC':
            return amount / float(btcrurasks[0][0])
        if output == 'LTC':
            return amount / float(ltcrurasks[0][0])
        if output == 'USD':
            return amount / usdrurasks[0][0]
        if output == 'EUR':
            return amount / float(eurrurasks[0][0])
    if currency == 'EUR':
        if output == 'BTC':
            return amount / float(btceurasks[0][0])
        if output == 'LTC':
            return amount / float(ltceurasks[0][0])
        if output == 'RUR':
            return amount * float(eurrurbids[0][0])
        if output == 'USD':
            return amount * float(eurusdbids[0][0])
    if currency == 'LTC':
        if output == 'BTC':
            return amount * float(ltcbtcbids[0][0])
        if output == 'EUR':
            return amount * float(ltceurbids[0][0])
        if output == 'USD':
            return amount * float(ltcusdbids[0][0])
        if output == 'NVC':
            amount *= float(ltcbtcbids[0][0])  # first convert to btc
            return amount / float(nvcbtcasks[0][0])
        if output == 'PPC':
            amount *= float(ltcusdbids[0][0])
            return amount / float(ppcusdasks[0][0])
        if output == 'RUR':
            return amount * float(ltcrurbids[0][0])
    if currency == 'NMC':
        return amount / nmcbtcbids[0][0]
    if currency == 'NVC':
        if output == 'BTC':
            return amount * float(nvcbtcbids[0][0])
        if output == 'LTC':
            amount *= float(nvcbtcbids[0][0])  #first convert to btc
            return amount / float(ltcbtcasks[0][0])
        if output == 'USD':
            return amount * float(nvcusdbids[0][0])
        if output == 'PPC':
            amount *= float(nvcusdbids[0][0])  # first in usd
            return amount / float(ppcusdasks[0][0])
    if currency == 'TRC':
        return amount / trcbtcbids[0][0]
    if currency == 'PPC':
        if output == 'LTC':
            amount = amount * float(ppcbtcbids[0][0])  # first convert to btc
            return amount / float(ltcbtcasks[0][0])
        if output == 'USD':
            return amount * float(ppcusdbids[0][0])
        if output == 'NVC':
            amount *= float(ppcusdbids[0][0])  # get it in usd
            return amount / float(nvcusdasks[0][0])
        if output == 'BTC':
            return amount * float(ppcbtcbids[0][0])
        if output == 'EUR':
            amount *= float(ppcusdbids[0][0])
            return amount / float(eurusdasks[0][0])
    if currency == 'FTC':
        return amount / ftcbtcbids[0][0]
    if currency == 'XPM':
        return amount / xpmbtcbids[0][0]


def get_current_usd():
    global current_usd
    handler = btceapi.KeyHandler(key_file, resaveOnDeletion=True)
    #key = 8CHAHTAA-9OINYFA3-C9SDDI4G-GW5ICB6X-MG941OT4
    #secret = 51b4938830ef003f2ecfabfec5b4b18cc9da2832f8888fb81bd14874c1f8442b
    for key in handler.getKeys():
        #print "#printing info for key %s" % key

        # NOTE: In future versions, the handler argument will be required.
        conn = btceapi.BTCEConnection()
        t = btceapi.TradeAPI(key, handler)

        try:
            r = t.getInfo(connection=conn)

            for currency in btceapi.all_currencies:
                ##print currency
                if currency == 'usd':
                    current_usd = float(getattr(r, "balance_" + currency))
                    current_usd *= 0.10  #get only half of the avalable money for usage
                    #print current_usd
                    ##print "\t%s balance: %s" % (currency.upper(), balance)
                '''
                #print "\tInformation rights: %r" % r.info_rights
                #print "\tTrading rights: %r" % r.trade_rights
                #print "\tWithrawal rights: %r" % r.withdraw_rights
                #print "\tServer time: %r" % r.server_time
                #print "\tItems in transaction history: %r" % r.transaction_count
                #print "\tNumber of open orders: %r" % r.open_orders
                #print "\topen orders:"
                orders = t.activeOrders(connection = conn)
                if orders:
                    for o in orders:
                        #print "\t\torder id: %r" % o.order_id
                        #print "\t\t    type: %s" % o.type
                        #print "\t\t    pair: %s" % o.pair
                        #print "\t\t    rate: %s" % o.rate
                        #print "\t\t  amount: %s" % o.amount
                        #print "\t\t created: %r" % o.timestamp_created
                        #print "\t\t  status: %r" % o.status
                        #print
                else:
                    #print "\t\tno orders"
                '''
        except Exception as e:
            logging.info("  An error occurred getting my current usd: %s" % e)
            pass
    threading.Timer(105, get_current_usd).start()


def get_the_most_recent_pairs():
    global ltcusdasks, ltcusdbids, ltcbtcasks, ltcbtcbids, btcusdasks, btcusdbids
    global nvcbtcasks, nvcbtcbids, nvcusdasks, nvcusdbids, ltceurasks, ltceurbids, ltcrurasks, ltcrurbids
    global eurrurasks, eurrurbids, ppcbtcasks, ppcbtcbids, ppcusdasks, ppcusdbids, eurusdasks, eurusdbids
    global btceurasks, btceurbids, btcrurasks, btcrurbids
    logging.info("getting the most recent pairs")
    try:
        pair = "ltc_usd"

        ltcusdasks, ltcusdbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*ltcusdasks)
        bid_prices, bid_volumes = zip(*ltcusdbids)

        pair = "ltc_btc"

        ltcbtcasks, ltcbtcbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*ltcbtcasks)
        bid_prices, bid_volumes = zip(*ltcbtcbids)

        pair = "btc_usd"

        btcusdasks, btcusdbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*btcusdasks)
        bid_prices, bid_volumes = zip(*btcusdbids)

        pair = "btc_eur"

        btceurasks, btceurbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*btceurasks)
        bid_prices, bid_volumes = zip(*btceurbids)

        pair = "btc_rur"

        btcrurasks, btcrurbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*btcrurasks)
        bid_prices, bid_volumes = zip(*btcrurbids)

        pair = "nvc_usd"

        nvcusdasks, nvcusdbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*nvcusdasks)
        bid_prices, bid_volumes = zip(*nvcusdbids)

        pair = "nvc_btc"

        nvcbtcasks, nvcbtcbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*nvcbtcasks)
        bid_prices, bid_volumes = zip(*nvcbtcbids)

        pair = "ltc_rur"

        ltcrurasks, ltcrurbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*ltcrurasks)
        bid_prices, bid_volumes = zip(*ltcrurbids)

        pair = "eur_rur"

        eurrurasks, eurrurbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*eurrurasks)
        bid_prices, bid_volumes = zip(*eurrurbids)

        pair = "eur_usd"

        eurusdasks, eurusdbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*eurusdasks)
        bid_prices, bid_volumes = zip(*eurusdbids)

        pair = "ltc_eur"

        ltceurasks, ltceurbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*ltceurasks)
        bid_prices, bid_volumes = zip(*ltceurbids)

        pair = "ppc_usd"

        ppcusdasks, ppcusdbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*ppcusdasks)
        bid_prices, bid_volumes = zip(*ppcusdbids)

        pair = "ppc_btc"

        ppcbtcasks, ppcbtcbids = btceapi.getDepth(pair)

        ask_prices, ask_volumes = zip(*ppcbtcasks)
        bid_prices, bid_volumes = zip(*ppcbtcbids)

        logging.info("i got them")
        print "i got them"
    except Exception as e:
        logging.info("  An error occurredwith getting the most recent pairs: %s" % e)
        print "i got error getting pairs"
        pass


def strategyone():
    threading.Timer(17 * random.random(), strategyone).start()
    get_the_most_recent_pairs()
    thisname = sys._getframe().f_code.co_name
    logger1.info(thisname)
    #this only works if first/usd and second/usd and first/second is possible
    #Example  of ['USD', 'LTC', ‘BTC’,’USD’]
    starting_money = current_usd
    logger1.info("starting money is" + str(starting_money))
    logger1.info("#LAPL = Lowest ask price of LTC/USD")
    LAPL = float(ltcusdasks[1][0])
    logger1.info(LAPL)
    logger1.info("#VL = Amount of LTC I can buy at that price")
    VL = float(ltcusdasks[1][1])
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPL * VL > starting_money:
        logger1.info("I dont have enough money to buy all the LTC so setting it to max")
        #starting money is less then the amount I can buy; setting VL to all of my starting money
        VL = starting_money / LAPL
    logger1.info("#VL = Amount of LTC I can buy at that price")
    logger1.info(VL)
    logger1.info("#HBPB = Highest bid price of LTC/BTC")
    HBPB = float(ltcbtcbids[1][0])
    logger1.info(HBPB)
    logger1.info("#VB = Amount of LTC I can sell  @ that price")
    VB = float(ltcbtcbids[1][1])
    logger1.info(VB)
    logger1.info("#HBPU = Highest bid price of BTC/USD")
    HBPU = float(btcusdbids[1][0])
    logger1.info(HBPU)
    logger1.info("#VU = Amount of BTC I CAN SELl at that price")
    VU = float(btcusdbids[1][1])
    logger1.info(VU)
    VU = return_equivalent('BTC', VU, 'LTC')
    logger1.info("#VU = Amount of BTC I CAN SELl at that price in a litecoin format")
    logger1.info(VU)
    maxv = min(VL, VB, VU)
    maxv = float(maxv)
    logger1.info("MY maxv that I can use is")
    logger1.info(maxv)

    logger1.info("#Buy an amount of Litecoins that is equal to maxv. This is my intial investment in dollars")
    cost = maxv * LAPL
    logger1.info(cost)
    logger1.info("#Caclualte fee")
    fee = maxv * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of Litecoins I receive is")
    amtlitecoin = maxv - fee
    logger1.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    logger1.info("#Amount of bitcoins I receive is")
    amtbitcoin = amtlitecoin * HBPB
    logger1.info(amtbitcoin)
    logger1.info("#Caclualte fee")
    fee = amtbitcoin * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of bitcoins I receive is")
    amtbitcoin -= fee
    logger1.info(amtbitcoin)
    logger1.info("#CONVERT MY  BITCION into USD")
    finalusd = amtbitcoin * HBPU
    logger1.info(finalusd)
    logger1.info("#Caclualte fee")
    fee = finalusd * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    logger1.info(finalusd)
    logger1.info("Profit is")
    logger1.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            logger1.info("this means its profitable and i should execute")
            logger1.info("doing first buy")
            z = trader.trade('ltc_usd', 'buy', float(ltcusdasks[1][0]), maxv)
            logger1.info("z.received" + str(z.received))
            logger1.info("z.remains" + str(z.remains))

            logger1.info("executing second")
            y = trader.trade('ltc_btc', 'sell', float(ltcbtcbids[1][0]), amtlitecoin)
            logger1.info("y.received" + str(y.received))
            logger1.info("y.remains" + str(y.remains))

            logger1.info("executing last")
            x = trader.trade('btc_usd', 'sell', float(btcusdbids[1][0]), amtbitcoin)
            logger1.info("x.received" + str(x.received))
            logger1.info("x.remains" + str(x.remains))

            if z.received == 0:
                trader.cancelOrder(z.order_id)
                logger1.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)
                logger1.info("I canceled the order")
                trader.trade('ltc_usd', 'sell', float(ltcusdbids[1][0], amtlitecoin))
                logger1.info("I reverted back to usd")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made tried to makea trade my homie.',
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            logger1.info("I executed my trades")

        do_trade()

    logger1.info("#VALID_PATH :  ['USD', 'NVC', ‘BTC’,’USD’]")
    #this only works if first/usd and second/usd and first/second is possible
    logger1.info("Starting strat 1-1")
    logger1.info("#LAPL = Lowest ask price of nvc/USD")
    LAPL = float(nvcusdasks[1][0])
    logger1.info(LAPL)
    logger1.info("#VL = Amount of nvc I can buy at that price")
    VL = float(nvcusdasks[1][1])
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPL * VL > starting_money:
        logger1.info("I dont have enough money to buy all the NVC so setting it to max")
        #starting money is less then the amount I can buy; setting VL to all of my starting money
        VL = starting_money / LAPL
    logger1.info("#VL = Amount of nvcI can buy at that price")
    logger1.info(VL)
    logger1.info("#HBPB = Highest bid price of BTC/nvc")
    HBPB = float(nvcbtcbids[1][0])
    logger1.info(HBPB)
    logger1.info("#VB = Amount of nvc I can sell  @ that price")
    VB = float(nvcbtcbids[1][1])
    logger1.info(VB)
    logger1.info("#HBPU = Highest bid price of USD/BTC")
    HBPU = float(btcusdbids[1][0])
    logger1.info(HBPU)
    logger1.info("#VU = Amount of BTC I CAN SELl at that price")
    VU = float(btcusdbids[1][1])
    logger1.info(VU)
    VU = return_equivalent('BTC', VU, 'NVC')
    logger1.info("#VU = Amount of BTC I CAN SELl at that price in a NVC format")
    logger1.info(VU)
    maxv = min(VL, VB, VU)
    maxv = float(maxv)
    logger1.info("MY maxv that I can use is")
    logger1.info(maxv)

    logger1.info("#Buy an amount of NVC that is equal to maxv. This is my intial investment in dollars")
    cost = maxv * LAPL
    logger1.info(cost)
    logger1.info("#Caclualte fee")
    fee = maxv * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of NVC I receive is")
    AMTNVC = maxv - fee
    logger1.info(AMTNVC)
    #Sell my litecoins into bitcoins
    logger1.info("#Amount of bitcoins I receive is")
    amtbitcoin = AMTNVC * HBPB
    logger1.info(amtbitcoin)
    logger1.info("#Caclualte fee")
    fee = amtbitcoin * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of bitcoins I receive is")
    amtbitcoin -= fee
    logger1.info(amtbitcoin)
    logger1.info("#CONVERT MY  BITCION into USD")
    finalusd = amtbitcoin * HBPU
    logger1.info(finalusd)
    logger1.info("#Caclualte fee")
    fee = finalusd * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    logger1.info(finalusd)
    logger1.info("Profit is")
    logger1.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            logger1.info("that means its profitable and I should execute")

            logger1.info("doing first trade")
            z = trader.trade('nvc_usd', 'buy', float(nvcusdasks[1][0]), maxv)
            logger1.info("x.received" + str(z.received))
            logger1.info("x.remains" + str(z.remains))

            logger1.info("doing second trade")
            y = trader.trade('nvc_btc', 'sell', float(nvcbtcbids[1][0]), AMTNVC)
            logger1.info("x.received" + str(y.received))
            logger1.info("x.remains" + str(y.remains))

            logger1.info("doing last trade")
            x = trader.trade('btc_usd', 'sell', float(btcusdbids[1][0]), amtbitcoin)
            logger1.info("x.received" + str(x.received))
            logger1.info("x.remains" + str(x.remains))

            if z.received == 0:
                trader.cancelOrder(z.order_id)
                logger1.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)
                logger1.info("I canceled the order")
                trader.trade('nvc_usd', 'sell', float(nvcusdbids[1][0]), AMTNVC)
                logger1.info("I reverted the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made tried to makea trade my homie.',
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            logger1.info("I executed my trades")

        do_trade()

    logger1.info("#VALID_PATH :  ['USD', 'ppc', ‘BTC’,’USD’]")
    logger1.info("Starting strat onetwo")
    starting_money = current_usd
    logger1.info("starting money is" + str(starting_money))
    logger1.info("#LAPP = Lowest ask price of ppc/USD")
    LAPP = float(ppcusdasks[1][0])
    logger1.info(LAPP)
    logger1.info("#VP = Amount of ppc I can buy at that price")
    VP = float(ppcusdasks[1][1])
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPP * VP > starting_money:
        logger1.info("I dont have enough money to buy all the ppc so setting it to max")
        #starting money is less then the amount I can buy; setting VP to all of my starting money
        VP = starting_money / LAPP
    logger1.info("#VP = Amount of ppc I can buy at that price")
    logger1.info(VP)
    logger1.info("#HBPB = Highest bid price of BTC/ppc")
    HBPB = float(ppcbtcbids[1][0])
    logger1.info(HBPB)
    logger1.info("#VB = Amount of ppc I can sell  @ that price")
    VB = float(ppcbtcbids[1][1])
    logger1.info(VB)
    logger1.info("#HBPU = Highest bid price of USD/BTC")
    HBPU = float(btcusdbids[1][0])
    logger1.info(HBPU)
    logger1.info("#VU = Amount of BTC I CAN SELl at that price")
    VU = float(btcusdbids[1][1])
    logger1.info(VU)
    VU /= (float(ppcbtcasks[1][0]))  # I do this so that all the volume is in ppc
    logger1.info("#VU = Amount of BTC I CAN SELl at that price in a ppc coins format")
    logger1.info(VU)
    maxv = min(VP, VB, VU)
    maxv = float(maxv)
    logger1.info("MY maxv that I can use is")
    logger1.info(maxv)

    logger1.info("#Buy an amount of ppc coinss that is equal to maxv. This is my intial investment in dollars")
    cost = maxv * LAPP
    logger1.info(cost)
    logger1.info("#Caclualte fee")
    fee = maxv * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of ppc coinss I receive is")
    amtppc = maxv - fee
    logger1.info(amtppc)
    #Sell my ppc coinss into bitcoins
    logger1.info("#Amount of bitcoins I receive is")
    amtbitcoin = amtppc * HBPB
    logger1.info(amtbitcoin)
    logger1.info("#Caclualte fee")
    fee = amtbitcoin * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of bitcoins I receive is")
    amtbitcoin -= fee
    logger1.info(amtbitcoin)
    logger1.info("#CONVERT MY  BITCION into USD")
    finalusd = amtbitcoin * HBPU
    logger1.info(finalusd)
    logger1.info("#Caclualte fee")
    fee = finalusd * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    logger1.info(finalusd)
    logger1.info("Profit is")
    logger1.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            logger1.info("that means its profitable and I should execute")

            logger1.info("doing first trade")
            z = trader.trade('ppc_usd', 'buy', float(ppcusdasks[1][0]), maxv)
            logger1.info("z.received" + str(z.received))
            logger1.info("z.remains" + str(z.remains))

            logger1.info("doing second trade")
            y = trader.trade('ppc_btc', 'sell', float(ppcbtcbids[1][0]), amtppc)
            logger1.info("y.received" + str(y.received))
            logger1.info("y.remains" + str(y.remains))

            logger1.info("doing third trade")
            x = trader.trade('btc_usd', 'sell', float(btcusdbids[1][0]), amtbitcoin)
            logger1.info("x.received" + str(x.received))
            logger1.info("x.remains" + str(x.remains))

            if z.received == 0:
                trader.cancelOrder(z.order_id)
                logger1.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)
                logger1.info("I canceled the order")
                trader.trade('ppc_usd', 'sell', float(ppcusdbids[1][0]), amtppc)
                logger1.info("I reversed the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made tried to makea trade my homie.',
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            logger1.info("I executed my trades")

        do_trade()

    logger1.info("# VALID_PATH :  ['USD', 'LTC', ‘EUR’,’USD’]")
    #this only works if first/usd and second/usd and first/second is possible
    logger1.info(thisname)
    starting_money = current_usd
    logger1.info("starting money is" + str(starting_money))
    logger1.info("#LAPL = Lowest ask price of LTC/USD")
    LAPL = float(ltcusdasks[1][0])
    logger1.info(LAPL)
    logger1.info("#VL = Amount of LTC I can buy at that price")
    VL = float(ltcusdasks[1][1])
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPL * VL > starting_money:
        logger1.info("I dont have enough money to buy all the LTC so setting it to max")
        #starting money is less then the amount I can buy; setting VL to all of my starting money
        VL = starting_money / LAPL
    logger1.info("#VL = Amount of LTC I can buy at that price")
    logger1.info(VL)
    logger1.info("#HBPB = Highest bid price of eur/LTC")
    HBPB = float(ltceurbids[1][0])
    logger1.info(HBPB)
    logger1.info("#VB = Amount of LTC I can sell  @ that price")
    VB = float(ltceurbids[1][1])
    logger1.info(VB)
    logger1.info("#HBPU = Highest bid price of USD/eur")
    HBPU = float(eurusdbids[1][0])
    logger1.info(HBPU)
    logger1.info("#VU = Amount of eur I CAN SELl at that price")
    VU = float(eurusdbids[1][1])
    logger1.info(VU)
    VU = return_equivalent('EUR', VU, 'LTC')
    logger1.info("#VU = Amount of EUR I CAN SELl at that price in a litecoin format")
    logger1.info(VU)
    maxv = min(VL, VB, VU)
    maxv = float(maxv)
    logger1.info("MY maxv that I can use is")
    logger1.info(maxv)

    logger1.info("#Buy an amount of Litecoins that is equal to maxv. This is my intial investment in dollars")
    cost = maxv * LAPL
    logger1.info(cost)
    logger1.info("#Caclualte fee")
    fee = maxv * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of Litecoins I receive is")
    amtlitecoin = maxv - fee
    logger1.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    logger1.info("#Amount of EURO I receive is")
    amtbitcoin = amtlitecoin * HBPB
    logger1.info(amtbitcoin)
    logger1.info("#Caclualte fee")
    fee = amtbitcoin * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of EURO I receive is")
    amtbitcoin -= fee
    logger1.info(amtbitcoin)
    logger1.info("#CONVERT MY  EURO into USD")
    finalusd = amtbitcoin * HBPU
    logger1.info(finalusd)
    logger1.info("#Caclualte fee")
    fee = finalusd * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    logger1.info(finalusd)
    logger1.info("Profit is")
    logger1.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        logger1.info("that means its profitable and I should execute")

        def do_trade():

            logger1.info("doing trade 1")
            z = trader.trade('ltc_usd', 'buy', float(ltcusdasks[1][0]), maxv)
            logger1.info("z.received" + str(z.received))
            logger1.info("z.remains" + str(z.remains))

            logger1.info("doing trade 2")
            y = trader.trade('ltc_eur', 'sell', float(ltceurbids[1][0]), amtlitecoin)
            logger1.info("y.received" + str(y.received))
            logger1.info("y.remains" + str(y.remains))

            logger1.info("doing trade 3")
            x = trader.trade('eur_usd', 'sell', float(eurusdbids[1][0]), amtbitcoin)
            logger1.info("x.received" + str(x.received))
            logger1.info("x.remains" + str(x.remains))

            if z.received == 0:
                trader.cancelOrder(z.order_id)
                logger1.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)
                logger1.info("I canceled the order")
                trader.trade('ltc_usd', 'sell', float(ltcusdbids[1][0]), amtlitecoin)
                logger1.info("i reversed the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made tried to makea trade my homie.',
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            logger1.info("I executed my trades")

        do_trade()

    logger1.info("#VALID_PATH :  ['USD', 'BTC', ‘EUR’,’USD’]")
    #this only works if first/usd and second/usd and first/second is possible
    starting_money = current_usd
    logger1.info("starting money is" + str(starting_money))
    logger1.info("#LAPL = Lowest ask price of BTC/USD")
    LAPL = float(btcusdasks[1][0])
    logger1.info(LAPL)
    logger1.info("#VL = Amount of BTC I can buy at that price")
    VL = float(btcusdasks[1][1])
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPL * VL > starting_money:
        logger1.info("I dont have enough money to buy all the btc so setting it to max")
        #starting money is less then the amount I can buy; setting VL to all of my starting money
        VL = starting_money / LAPL
    logger1.info("#VL = Amount of EUR I can buy at that price")
    logger1.info(VL)
    logger1.info("#HBPB = Highest bid price of eur/BTC")
    HBPB = float(btceurbids[1][0])
    logger1.info(HBPB)
    logger1.info("#VB = Amount of BTC I can sell  @ that price")
    VB = float(btceurbids[1][1])
    logger1.info(VB)
    logger1.info("#HBPU = Highest bid price of USD/eur")
    HBPU = float(eurusdbids[1][0])
    logger1.info(HBPU)
    logger1.info("#VU = Amount of eur I CAN SELl at that price")
    VU = float(eurusdbids[1][1])
    logger1.info(VU)
    VU = return_equivalent('EUR', VU, 'BTC')
    logger1.info("#VU = Amount of EUR I CAN SELl at that price in a btc format")
    logger1.info(VU)
    maxv = min(VL, VB, VU)
    maxv = float(maxv)
    logger1.info("MY maxv that I can use is")
    logger1.info(maxv)

    logger1.info("#Buy an amount of BTC that is equal to maxv. This is my intial investment in dollars")
    cost = maxv * LAPL
    logger1.info(cost)
    logger1.info("#Caclualte fee")
    fee = maxv * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of BTC I receive is")
    amtlitecoin = maxv - fee
    logger1.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    logger1.info("#Amount of EURO I receive is")
    amtbitcoin = amtlitecoin * HBPB
    logger1.info(amtbitcoin)
    logger1.info("#Caclualte fee")
    fee = amtbitcoin * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("#Amount of EURO I receive is")
    amtbitcoin -= fee
    logger1.info(amtbitcoin)
    logger1.info("#CONVERT MY  EURO into USD")
    finalusd = amtbitcoin * HBPU
    logger1.info(finalusd)
    logger1.info("#Caclualte fee")
    fee = finalusd * 0.002
    logger1.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        logger1.info("fee was less then minimum")
        fee = 0.0001
    logger1.info(fee)
    logger1.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    logger1.info(finalusd)
    logger1.info("Profit is")
    logger1.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            logger1.info("that means its profitable and I should execute")
            logger1.info("doing trade 1")
            z = trader.trade('btc_usd', 'buy', float(btcusdasks[1][0]), maxv)
            logger1.info("z.received" + str(z.received))
            logger1.info("z.remains" + str(z.remains))

            logger1.info("doingtrade 2")
            y = trader.trade('btc_eur', 'sell', float(btceurbids[1][0]), amtlitecoin)
            logger1.info("y.received" + str(y.received))
            logger1.info("y.remains" + str(y.remains))

            logger1.info("doing trade 3")
            x = trader.trade('eur_usd', 'sell', float(eurusdbids[1][0]), amtbitcoin)
            logger1.info("x.received" + str(x.received))
            logger1.info("x.remains" + str(x.remains))

            if z.received == 0:
                trader.cancelOrder(z.order_id)
                logger1.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)
                logger1.info("I canceled the order")
                trader.trade('btc_usd', 'sell', float(btcusdbids[1][0]), amtlitecoin)
                logger1.info("i reversed the orderd")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes',
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made tried to makea trade my homie.',
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            logger1.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'LTC', 'BTC', ‘NVC’, ’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcbtc"
    pair3 = "nvcbtc"
    pair4 = "nvcusd"
    #has to be first/usd, first/second, third/second, third/usd
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + " into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")
            loggerstrat2.info("doing first trade")
            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received" + str(z.received))
            loggerstrat2.info("x.remains" + str(z.remains))

            loggerstrat2.info("doing second trade")
            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(y.received))
            loggerstrat2.info("x.remains" + str(y.remains))

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            loggerstrat2.info("doing last trade")
            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(w.received))
            loggerstrat2.info("x.remains" + str(w.remains))

            if z.received == 0:
                trader.cancelOrder(z.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='1yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)
                loggerstrat2.info("I canceled the order")
                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[1][0]')), amtlitecoin)
                loggerstrat2.info("I reversed the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='2yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you went through a trade homes' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("VALID_PATH :  ['USD', 'LTC', 'EUR', ‘BTC’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "btcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg i did a trade homes' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'BTC', 'EUR', ‘LTC’,’USD’]")
    pair1 = "btcusd"
    pair2 = "btceur"
    pair3 = "ltceur"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you tried to make some trades but hte got canceled my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you tried to make some trades but hte got canceled my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you tried to make some trades but hte got canceled my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'PPC', 'BTC', ‘LTC’,’USD’]")
    pair1 = "ppcusd"
    pair2 = "ppcbtc"
    pair3 = "ltcbtc"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you cancedl a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you cancedl a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you cancedl a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'NVC', 'BTC', ‘LTC’,’USD’’]")
    pair1 = "nvcusd"
    pair2 = "nvcbtc"
    pair3 = "ltcbtc"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I cnacled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I cnacled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I cnacled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'LTC', 'BTC', ‘PPC’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcbtc"
    pair3 = "ppcbtc"
    pair4 = "ppcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'NVC', 'BTC', ‘PPC’,’USD’]")
    pair1 = "nvcusd"
    pair2 = "nvcbtc"
    pair3 = "ppcbtc"
    pair4 = "ppcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'PPC', 'BTC', ‘NVC’,’USD’]")
    pair1 = "ppcusd"
    pair2 = "ppcbtc"
    pair3 = "nvcbtc"
    pair4 = "nvcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  PATH :  ['USD', 'LTC', 'RUR', ‘BTC’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "btcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  PATH :  VALID_PATH :  ['USD', 'BTC', 'RUR', ‘LTC’,’USD’]")
    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "ltcrur"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("VALID_PATH :  ['USD', 'EUR', 'RUR', ‘LTC’,’USD’]")
    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "ltcrur"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH : ['USD', 'BTC', 'RUR', ‘EUR’,’USD’]")
    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "eurrur"
    pair4 = "eurusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat2.info("#VALID_PATH :  ['USD', 'LTC', 'RUR', ‘EUR’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "eurrur"
    pair4 = "eurusd"
    #has to be first/usd, first/second, third/second, third/us
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into rur
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #buy euro from rur
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my eur TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat2.info("that means its profitable and I should execute")

            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat2.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[1][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat2.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :  ['USD', 'LTC', 'RUR', 'EUR', ‘BTC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "eurrur"
    pair4 = "btceur"
    pair5 = "btcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :  ['USD', 'BTC', 'RUR', 'EUR', ‘LTC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "eurrur"
    pair4 = "ltceur"
    pair5 = "ltcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :  ['USD', 'EUR', 'RUR', 'BTC', ‘LTC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "btcrur"
    pair4 = "ltcbtc"
    pair5 = "ltcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd

    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :  ['USD', 'LTC', 'RUR', 'BTC', ‘PPC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :['USD', 'LTC', 'EUR', 'BTC', ‘PPC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :  ['USD', 'EUR', 'RUR', 'BTC', ‘PPC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "btcrur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info("VALID_PATH :  ['USD', 'LTC', 'RUR', 'BTC', ‘NVC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "nvcbtc"
    pair5 = "nvcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()

    loggerstrat9.info(" VALID_PATH :  ['USD', 'LTC', 'EUR', 'BTC', ‘NVC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "nvcbtc"
    pair5 = "nvcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1 + 'asks[1][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        def do_trade():
            loggerstrat9.info("that means its profitable and I should execute")

            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[1][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[1][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[1][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[1][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[1][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            if x.received == 0:
                trader.cancelOrder(x.order_id)
                loggerstrat9.info("I canceled the order")
                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[1][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')
            loggerstrat9.info("I executed my trades")

        do_trade()


'''
def strategytwo():
    threading.Timer(15, strategytwo).start()
    get_the_most_recent_pairs()
    thisname = sys._getframe().f_code.co_name
    loggerstrat2.info("#VALID_PATH :  ['USD', 'LTC', 'BTC', ‘NVC’, ’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcbtc"
    pair3 = "nvcbtc"
    pair4 = "nvcusd"
    #has to be first/usd, first/second, third/second, third/usd
    loggerstrat2.info(thisname)
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + " into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("VALID_PATH :  ['USD', 'LTC', 'EUR', ‘BTC’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "btcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'BTC', 'EUR', ‘LTC’,’USD’]")
    pair1 = "btcusd"
    pair2 = "btceur"
    pair3 = "ltceur"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'PPC', 'BTC', ‘LTC’,’USD’]")
    pair1 = "ppcusd"
    pair2 = "ppcbtc"
    pair3 = "ltcbtc"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'NVC', 'BTC', ‘LTC’,’USD’’]")
    pair1 = "nvcusd"
    pair2 = "nvcbtc"
    pair3 = "ltcbtc"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(4)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(4)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(4)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received" + str(x.received))
            loggerstrat2.info("x.remains" + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'LTC', 'BTC', ‘PPC’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcbtc"
    pair3 = "ppcbtc"
    pair4 = "ppcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'NVC', 'BTC', ‘PPC’,’USD’]")
    pair1 = "nvcusd"
    pair2 = "nvcbtc"
    pair3 = "ppcbtc"
    pair4 = "ppcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'PPC', 'BTC', ‘NVC’,’USD’]")
    pair1 = "ppcusd"
    pair2 = "ppcbtc"
    pair3 = "nvcbtc"
    pair4 = "nvcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  PATH :  ['USD', 'LTC', 'RUR', ‘BTC’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "btcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  PATH :  VALID_PATH :  ['USD', 'BTC', 'RUR', ‘LTC’,’USD’]")
    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "ltcrur"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("VALID_PATH :  ['USD', 'EUR', 'RUR', ‘LTC’,’USD’]")
    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "ltcrur"
    pair4 = "ltcusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH : ['USD', 'BTC', 'RUR', ‘EUR’,’USD’]")
    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "eurrur"
    pair4 = "eurusd"
    #has to be first/usd, first/second, third/second, third/usd
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into bitcoins
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #sell my bitcoins into NVC
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my NVC TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")

    loggerstrat2.info("#VALID_PATH :  ['USD', 'LTC', 'RUR', ‘EUR’,’USD’]")
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "eurrur"
    pair4 = "eurusd"
    #has to be first/usd, first/second, third/second, third/us
    starting_money = current_usd
    loggerstrat2.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)
    loggerstrat2.info("My maxV is " + str(maxv))

    loggerstrat2.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat2.info(cost)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat2.info(amtlitecoin)
    #Sell my litecoins into rur
    loggerstrat2.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat2.info(amtbitcoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat2.info(amtbitcoin)
    #buy euro from rur
    loggerstrat2.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat2.info(amtnvccoin)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat2.info(fee)
    loggerstrat2.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat2.info(amtnvccoin)

    #Sell my eur TO USD
    loggerstrat2.info("#CONVERT MY " + pair4[:3] + "  into USD")
    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())
    loggerstrat2.info(finalusd)
    loggerstrat2.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat2.info(fee)
    loggerstrat2.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat2.info(finalusd)
    loggerstrat2.info("Profit is")
    loggerstrat2.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat2.info("that means its profitable and I should execute")
        try:
            loggerstrat2.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat2.info("I canceled the order")
            return
        try:
            loggerstrat2.info("doing last trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat2.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)
            loggerstrat2.info("x.received " + str(x.received))
            loggerstrat2.info("x.remains " + str(x.remains))
            pass

        loggerstrat2.info("I executed my trades")


#def strategythree():
    #print("shit")
    #VALID_PATH :  ['USD', 'EUR', 'LTC', ‘BTC’,’USD’]
    #fits first/usd, second/first, second/third, third/usd


def strategyfour():
    thisname = sys._getframe().f_code.co_name
    #VALID_PATH :  ['USD', 'EUR', ‘BTC’,’USD’]
    pair1 = "eurusd"
    pair2 = "btceur"
    pair3 = "btcusd"
    #fits first/usd, second/first, second/ usd
    #print("Starting strat four")
    loggerstrat4.info("Starting strat four")
    starting_money = current_usd
    loggerstrat4.info("starting money is" + str(starting_money))
    loggerstrat4.info("#LAPE = Lowest ask price of eur/usd")

    #MEEDS TO BE FIXED BELOW THIS
    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3)
    LAPE = float(eurusdasks[0][0])
    loggerstrat4.info(LAPE)
    loggerstrat4.info("#VE = Amount of EUR I can buy at that price")
    VE = float(eurusdasks[0][1])
    #Check to make sure that the amount I can buy is less than my starting money
    if LAPE*VE > starting_money:
        loggerstrat4.info("I dont have enough money to buy all the ppc so setting it to max")
        #starting money is less then the amount I can buy; setting VE to all of my starting money
        VE = starting_money/LAPE
    loggerstrat4.info("#VE = Amount of EUR I can buy at that price")
    loggerstrat4.info(VE)
    loggerstrat4.info("#HBPB = Lowest ask price price of BTC/Eur")
    HBPB = float(btceurasks[0][0])
    loggerstrat4.info(HBPB)
    loggerstrat4.info("#VB = Amount of BTC I can buy  @ that price")
    VB = float(btceurasks[0][1])
    loggerstrat4.info(VB)
    loggerstrat4.info("IN euro format that is")
    VB = float(btceurasks[0][0])*VB
    loggerstrat4.info(VB)
    loggerstrat4.info("#HBPU = Highest bid price of USD/BTC")
    HBPU = float(btcusdbids[0][0])
    loggerstrat4.info(HBPU)
    loggerstrat4.info("#VU = Amount of BTC I CAN SELl at that price")
    VU = float(btcusdbids[0][1])
    loggerstrat4.info(VU)
    VU = VU*(float(btceurasks[0][0])) # I do this so that all the volume is in eur
    loggerstrat4.info("#VU = Amount of BTC I CAN SELl at that price in a eur format")
    loggerstrat4.info(VU)
    maxv = min(VE, VB, VU)
    maxv = float(maxv)
    loggerstrat4.info("MY maxv that I can use is")
    loggerstrat4.info(maxv)

    loggerstrat4.info("#Buy an Amount of EUR coinss that is equal to maxv. This is my intial investment in dollars")
    cost = maxv * LAPE
    loggerstrat4.info(cost)
    loggerstrat4.info("#Caclualte fee")
    fee = maxv * 0.002
    loggerstrat4.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        loggerstrat4.info("fee was less then minimum")
        fee = 0.0001
    loggerstrat4.info(fee)
    loggerstrat4.info("#Amount of EUR coinss I receive is")
    AMTeur = maxv - fee
    loggerstrat4.info(AMTeur)
    #Sell my eur coinss into bitcoins
    loggerstrat4.info("#Amount of bitcoins I receive is")
    amtbitcoin = AMTeur / HBPB
    loggerstrat4.info(amtbitcoin)
    loggerstrat4.info("#Caclualte fee")
    fee = amtbitcoin * 0.002
    loggerstrat4.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        loggerstrat4.info("fee was less then minimum")
        fee = 0.0001
    loggerstrat4.info(fee)
    loggerstrat4.info("#Amount of bitcoins I receive is")
    amtbitcoin -= fee
    loggerstrat4.info(amtbitcoin)
    loggerstrat4.info("#CONVERT MY  BITCION into USD")
    finalusd = amtbitcoin*HBPU
    loggerstrat4.info(finalusd)
    loggerstrat4.info("#Caclualte fee")
    fee = finalusd * 0.002
    loggerstrat4.info(fee)
    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        loggerstrat4.info("fee was less then minimum")
        fee = 0.0001
    loggerstrat4.info(fee)
    loggerstrat4.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat4.info(finalusd)
    loggerstrat4.info("Profit is")
    loggerstrat4.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        try:
            loggerstrat4.info("that means its profitable and I should execute")
            x = trader.trade('eur_usd', 'buy', float(eurusdasks[0][0]), maxv)
        except Exception as e:
            loggerstrat4.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade('eur_usd', 'buy', float(eurusdasks[0][0]), maxv)
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            return
        try:
            time.sleep(3)
            x = trader.trade('btc_eur', 'buy', float(btceurasks[0][0]), AMTeur)
        except Exception as e:
            loggerstrat4.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade('btc_eur', 'buy', float(btceurasks[0][0]), AMTeur)
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            return
        try:
            time.sleep(3)
            x = trader.trade('btc_usd', 'sell', float(btcusdbids[0][0]), amtbitcoin)
        except Exception as e:
            loggerstrat4.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade('btc_usd', 'sell', float(btcusdbids[0][0]), amtbitcoin)
            pass

        loggerstrat4.info("I executed my trades")
    threading.Timer(23, strategyfour).start()



#def strategyfive():
    #print("shit")
    #VALID_PATH :  ['USD', 'EUR', 'RUR', ‘BTC’,’USD’]
    #fits first/usd, first/second, third/second, third/usd


#def strategysix():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'RUR', ‘BTC’,’USD’]
    #usd/first,second/first, second/usd


#def strategyseven():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'RUR', 'LTC', ‘BTC’,’USD’]
    #usd/first, second/first,second/third,third/usd


#def strategyeight():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'RUR', 'EUR', ‘BTC’,’USD’]
    #usd/first, second/first, third/second, third/usd

def strategynine():
    get_the_most_recent_pairs()
    threading.Timer(25, strategynine).start()
    loggerstrat9.info("VALID_PATH :  ['USD', 'LTC', 'RUR', 'EUR', ‘BTC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    thisname = sys._getframe().f_code.co_name
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "eurrur"
    pair4 = "btceur"
    pair5 = "btcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    loggerstrat9.info(thisname)
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")

    loggerstrat9.info("VALID_PATH :  ['USD', 'BTC', 'RUR', 'EUR', ‘LTC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "eurrur"
    pair4 = "ltceur"
    pair5 = "ltcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")

    loggerstrat9.info("VALID_PATH :  ['USD', 'EUR', 'RUR', 'BTC', ‘LTC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "btcrur"
    pair4 = "ltcbtc"
    pair5 = "ltcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd

    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")


    loggerstrat9.info("VALID_PATH :  ['USD', 'LTC', 'RUR', 'BTC', ‘PPC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")

    loggerstrat9.info("VALID_PATH :['USD', 'LTC', 'EUR', 'BTC', ‘PPC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")

    loggerstrat9.info("VALID_PATH :  ['USD', 'EUR', 'RUR', 'BTC', ‘PPC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "btcrur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")

    loggerstrat9.info("VALID_PATH :  ['USD', 'LTC', 'RUR', 'BTC', ‘NVC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "nvcbtc"
    pair5 = "nvcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")

    loggerstrat9.info(" VALID_PATH :  ['USD', 'LTC', 'EUR', 'BTC', ‘NVC’,’USD’]")
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "nvcbtc"
    pair5 = "nvcusd"
    #first/usd, first/second,third/second,fourth/third,fourth/usd
    starting_money = current_usd
    loggerstrat9.info("starting money is" + str(starting_money))
    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)
    loggerstrat9.info("My maxV is " + str(maxv))

    loggerstrat9.info("#Buy an amount of " + pair1 + " that is equal to maxv. This is my intial investment in dollars")
    cost = float(eval(pair1+'asks[0][0]')) * maxv
    loggerstrat9.info(cost)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(maxv)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair1[:3] + " I receive is")
    amtlitecoin = maxv - fee
    loggerstrat9.info(amtlitecoin)
    #Sell my litecion in rur
    loggerstrat9.info("#Amount of " + pair2[3:] + " I receive is")
    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())
    loggerstrat9.info(amtbitcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtbitcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair2[3:].upper() + " I receive is")
    amtbitcoin -= fee
    loggerstrat9.info(amtbitcoin)
    #Buy euro using rur
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())
    loggerstrat9.info(amtnvccoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtnvccoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair3[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtnvccoin)
    #Buy btc using euro
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())
    loggerstrat9.info(amtdickcoin)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(amtdickcoin)
    loggerstrat9.info(fee)
    loggerstrat9.info("#Amount of " + pair4[:3] + " I receive is")
    amtnvccoin -= fee
    loggerstrat9.info(amtdickcoin)

    #Sell my BTC TO USD
    loggerstrat9.info("#CONVERT MY " + pair5[:3] + "  into USD")
    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())
    loggerstrat9.info(finalusd)
    loggerstrat9.info("#Caclualte fee")
    fee = calculate_fee(finalusd)
    loggerstrat9.info(fee)
    loggerstrat9.info("MY FINAL ENDING MONEY IS")
    finalusd -= fee
    loggerstrat9.info(finalusd)
    loggerstrat9.info("Profit is")
    loggerstrat9.info(finalusd - cost)
    print(str(finalusd - cost))
    if finalusd > cost:
        sendemail(from_addr = 'shemer77@gmail.com',
          to_addr_list = ['shemer77@gmail.com'],
          cc_addr_list = '',
          subject      = thisname,
          message      = 'yo dawg you made a trade my homie',
          login        = 'shemer77',
          password     = 'augedqrdvoplyqjm')
        loggerstrat9.info("that means its profitable and I should execute")
        try:
            loggerstrat9.info("doing first trade")
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair1[:3]+'_'+pair1[3:], 'buy', float(eval(pair1+'asks[0][0]')), maxv)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing second trade")
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair2[:3]+'_'+pair2[3:], 'sell', float(eval(pair2+'bids[0][0]')), amtlitecoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing third trade")
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')), amtbitcoin/float(eval(pair3 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing fourth trade")
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')), amtnvccoin/float(eval(pair4 + 'asks[0][0]')))
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
            pass
        if x.received == 0:
            trader.cancelOrder(x.order_id)
            loggerstrat9.info("I canceled the order")
            return
        try:
            loggerstrat9.info("doing last trade")
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))
        except Exception as e:
            loggerstrat9.info("  An error occurred: %s" % e)
            time.sleep(3)
            x = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)
            loggerstrat9.info("x.received " + str(x.received))
            loggerstrat9.info("x.remains " + str(x.remains))

        loggerstrat9.info("I executed my trades")


#def strategyten():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'LTC', 'EUR', 'RUR', ‘BTC’,’USD’]
    #first/usd, first/second, second/third, fourth/third, fourth/usd


#def strategyeleven():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'EUR', 'LTC', 'RUR', ‘BTC’,’USD’]
    #first/usd, second/first,second/third, fourth/third, fourth/usd


#def strategytweleve():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'EUR', 'RUR', 'LTC', ‘BTC’,’USD’]
    #first/usd, first/second, third/second,third/fourth, fourth/usd


#def strategythirteen():
    #print("SHIT")
    # VALID_PATH :  ['USD', 'RUR', 'LTC', 'EUR', ‘BTC’,’USD’]
    #usd/first, second/first, second/third, fourth/third, fourth/usd


#def strategyfourteen():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'RUR', 'EUR', 'LTC', ‘BTC’,’USD’]
    #usd/first, second/first, third/second, third/fourth, fourth/usd


#def strategyfifteen():
    #print("SHIT")
    # VALID_PATH :  ['USD', 'EUR', 'BTC', ‘LTC’,’USD’]
    #first/usd, second/first, third/second, third/usd


#def strategysixteen():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'PPC', 'BTC', 'RUR', 'EUR', ‘LTC’,’USD’]
    #first/usd, first/second, second/thrid, fourth/third, fifth/fourth, fifth/usd

#def strategysevteen():
    #print("SHIT")
    #VALID_PATH :  ['USD', 'PPC', 'BTC', 'EUR', 'RUR', ‘LTC’,’USD’]
    #first/usd, first/second, second/third, third/fourth, fifth/fourth, fifth/usd

'''


def intiliaze_trader():
    global trader
    handler = btceapi.KeyHandler(key_file, resaveOnDeletion=True)
    logging.info(handler.keys)
    trader = btceapi.TradeAPI(handler.keys[0], handler)
    #x = trader.trade('ltc_usd','buy',float(0.1),maxv)


intiliaze_trader()
get_current_usd()

strategyone()
#strategyonefive()

#strategytwo()



#strategyfour()

#strategynine()
