key_file = 'btce.txt'


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

    LAPL = float(eval(pair1 + 'asks[0][0]'))

    VL = float(eval(pair1 + 'asks[0][1]'))

    if LAPL * VL > starting_money:
        VL = starting_money / LAPL

    VB = float(eval(pair2 + 'bids[0][1]'))

    VN = float(eval(pair3 + 'asks[0][1]'))

    VN = return_equivalent(pair3[:3].upper(), VN, pair1[:3].upper())

    VU = float(eval(pair4 + 'bids[0][1]'))

    VU = return_equivalent(pair4[:3].upper(), VU, pair1[:3].upper())

    maxv = min(VL, VB, VU, VN)
    maxv = float(maxv)

    return maxv


def get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5):
    pair1 = str(pair1)
    pair2 = str(pair2)
    pair3 = str(pair3)
    pair4 = str(pair4)
    pair5 = str(pair5)
    starting_money = current_usd

    LAPL = float(eval(pair1 + 'asks[0][0]'))

    VL = float(eval(pair1 + 'asks[0][1]'))

    if LAPL * VL > starting_money:
        VL = starting_money / LAPL

    VB = float(eval(pair2 + 'bids[0][1]'))

    VN = float(eval(pair3 + 'asks[0][1]'))

    VN = return_equivalent(pair3[:3].upper(), VN, pair1[:3].upper())

    VG = float(eval(pair4 + 'asks[0][1]'))

    VG = return_equivalent(pair4[:3].upper(), VG, pair1[:3].upper())

    VU = float(eval(pair5 + 'bids[0][1]'))

    VU = return_equivalent(pair5[:3].upper(), VU, pair1[:3].upper())

    maxv = min(VL, VB, VU, VN, VG)
    maxv = float(maxv)

    return maxv


def return_equivalent(currency, amount, output):
    if currency == 'USD':
        if output == 'BTC':
            return amount / float(btcusdasks[0][0])
        if output == 'LTC':
            return amount / ltcusdasks[0][0]

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
            amount *= float(ltcbtcbids[0][0])
            return amount / float(nvcbtcasks[0][0])
        if output == 'PPC':
            amount *= float(ltcusdbids[0][0])
            return amount / float(ppcusdasks[0][0])
        if output == 'RUR':
            return amount * float(ltcrurbids[0][0])

    if currency == 'NVC':
        if output == 'BTC':
            return amount * float(nvcbtcbids[0][0])
        if output == 'LTC':
            amount *= float(nvcbtcbids[0][0])
            return amount / float(ltcbtcasks[0][0])
        if output == 'USD':
            return amount * float(nvcusdbids[0][0])
        if output == 'PPC':
            amount *= float(nvcusdbids[0][0])
            return amount / float(ppcusdasks[0][0])

    if currency == 'PPC':
        if output == 'LTC':
            amount = amount * float(ppcbtcbids[0][0])
            return amount / float(ltcbtcasks[0][0])
        if output == 'USD':
            return amount * float(ppcusdbids[0][0])
        if output == 'NVC':
            amount *= float(ppcusdbids[0][0])
            return amount / float(nvcusdasks[0][0])
        if output == 'BTC':
            return amount * float(ppcbtcbids[0][0])
        if output == 'EUR':
            amount *= float(ppcusdbids[0][0])
            return amount / float(eurusdasks[0][0])


def get_current_usd():
    global current_usd
    handler = btceapi.KeyHandler(key_file, resaveOnDeletion=True)

    for key in handler.getKeys():


        conn = btceapi.BTCEConnection()
        t = btceapi.TradeAPI(key, handler)

        try:
            r = t.getInfo(connection=conn)

            for currency in btceapi.all_currencies:

                if currency == 'usd':
                    current_usd = float(getattr(r, "balance_" + currency))
                    current_usd *= 0.10

        except Exception:

            pass
    threading.Timer(100, get_current_usd).start()


def get_the_most_recent_pairs():
    global ltcusdasks, ltcusdbids, ltcbtcasks, ltcbtcbids, btcusdasks, btcusdbids
    global nvcbtcasks, nvcbtcbids, nvcusdasks, nvcusdbids, ltceurasks, ltceurbids, ltcrurasks, ltcrurbids
    global eurrurasks, eurrurbids, ppcbtcasks, ppcbtcbids, ppcusdasks, ppcusdbids, eurusdasks, eurusdbids
    global btceurasks, btceurbids, btcrurasks, btcrurbids

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



    except Exception:


        pass


def strategyone():
    threading.Timer(17 * random.random(), strategyone).start()
    get_the_most_recent_pairs()
    thisname = sys._getframe().f_code.co_name

    starting_money = current_usd

    LAPL = float(ltcusdasks[0][0])

    VL = float(ltcusdasks[0][1])

    if LAPL * VL > starting_money:
        VL = starting_money / LAPL

    HBPB = float(ltcbtcbids[0][0])

    VB = float(ltcbtcbids[0][1])

    HBPU = float(btcusdbids[0][0])

    VU = float(btcusdbids[0][1])

    VU = return_equivalent('BTC', VU, 'LTC')

    maxv = min(VL, VB, VU)
    maxv = float(maxv)

    cost = maxv * LAPL

    fee = maxv * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        fee = 0.0001

    amtlitecoin = maxv - fee

    amtbitcoin = amtlitecoin * HBPB

    fee = amtbitcoin * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    amtbitcoin -= fee

    finalusd = amtbitcoin * HBPU

    fee = finalusd * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade('ltc_usd', 'buy', float(ltcusdasks[0][0]), maxv)

            y = trader.trade('ltc_btc', 'sell', float(ltcbtcbids[0][0]), amtlitecoin)

            x = trader.trade('btc_usd', 'sell', float(btcusdbids[0][0]), amtbitcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

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

                trader.trade('ltc_usd', 'sell', float(ltcusdbids[0][0]), amtlitecoin)

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

        do_trade()

    LAPL = float(nvcusdasks[0][0])

    VL = float(nvcusdasks[0][1])

    if LAPL * VL > starting_money:
        VL = starting_money / LAPL

    HBPB = float(nvcbtcbids[0][0])

    VB = float(nvcbtcbids[0][1])

    HBPU = float(btcusdbids[0][0])

    VU = float(btcusdbids[0][1])

    VU = return_equivalent('BTC', VU, 'NVC')

    maxv = min(VL, VB, VU)
    maxv = float(maxv)

    cost = maxv * LAPL

    fee = maxv * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        fee = 0.0001

    AMTNVC = maxv - fee

    amtbitcoin = AMTNVC * HBPB

    fee = amtbitcoin * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    amtbitcoin -= fee

    finalusd = amtbitcoin * HBPU

    fee = finalusd * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade('nvc_usd', 'buy', float(nvcusdasks[0][0]), maxv)

            y = trader.trade('nvc_btc', 'sell', float(nvcbtcbids[0][0]), AMTNVC)

            x = trader.trade('btc_usd', 'sell', float(btcusdbids[0][0]), amtbitcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

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

                trader.trade('nvc_usd', 'sell', float(nvcusdbids[0][0]), AMTNVC)

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


        do_trade()

    starting_money = current_usd

    LAPP = float(ppcusdasks[0][0])

    VP = float(ppcusdasks[0][1])

    if LAPP * VP > starting_money:
        VP = starting_money / LAPP

    HBPB = float(ppcbtcbids[0][0])

    VB = float(ppcbtcbids[0][1])

    HBPU = float(btcusdbids[0][0])

    VU = float(btcusdbids[0][1])

    VU /= (float(ppcbtcasks[0][0]))

    maxv = min(VP, VB, VU)
    maxv = float(maxv)

    cost = maxv * LAPP

    fee = maxv * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        fee = 0.0001

    amtppc = maxv - fee

    amtbitcoin = amtppc * HBPB

    fee = amtbitcoin * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    amtbitcoin -= fee

    finalusd = amtbitcoin * HBPU

    fee = finalusd * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade('ppc_usd', 'buy', float(ppcusdasks[0][0]), maxv)

            y = trader.trade('ppc_btc', 'sell', float(ppcbtcbids[0][0]), amtppc)

            x = trader.trade('btc_usd', 'sell', float(btcusdbids[0][0]), amtbitcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

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

                trader.trade('ppc_usd', 'sell', float(ppcusdbids[0][0]), amtppc)

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

        do_trade()

    starting_money = current_usd

    LAPL = float(ltcusdasks[0][0])

    VL = float(ltcusdasks[0][1])

    if LAPL * VL > starting_money:
        VL = starting_money / LAPL

    HBPB = float(ltceurbids[0][0])

    VB = float(ltceurbids[0][1])

    HBPU = float(eurusdbids[0][0])

    VU = float(eurusdbids[0][1])

    VU = return_equivalent('EUR', VU, 'LTC')

    maxv = min(VL, VB, VU)
    maxv = float(maxv)

    cost = maxv * LAPL

    fee = maxv * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        fee = 0.0001

    amtlitecoin = maxv - fee

    amtbitcoin = amtlitecoin * HBPB

    fee = amtbitcoin * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    amtbitcoin -= fee

    finalusd = amtbitcoin * HBPU

    fee = finalusd * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    finalusd -= fee

    if finalusd > cost:

        def do_trade():


            z = trader.trade('ltc_usd', 'buy', float(ltcusdasks[0][0]), maxv)

            y = trader.trade('ltc_eur', 'sell', float(ltceurbids[0][0]), amtlitecoin)

            x = trader.trade('eur_usd', 'sell', float(eurusdbids[0][0]), amtbitcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

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

                trader.trade('ltc_usd', 'sell', float(ltcusdbids[0][0]), amtlitecoin)

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

        do_trade()

    starting_money = current_usd

    LAPL = float(btcusdasks[0][0])

    VL = float(btcusdasks[0][1])

    if LAPL * VL > starting_money:
        VL = starting_money / LAPL

    HBPB = float(btceurbids[0][0])

    VB = float(btceurbids[0][1])

    HBPU = float(eurusdbids[0][0])

    VU = float(eurusdbids[0][1])

    VU = return_equivalent('EUR', VU, 'BTC')

    maxv = min(VL, VB, VU)
    maxv = float(maxv)

    cost = maxv * LAPL

    fee = maxv * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee < 0.0001:
        fee = 0.0001

    amtlitecoin = maxv - fee

    amtbitcoin = amtlitecoin * HBPB

    fee = amtbitcoin * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    amtbitcoin -= fee

    finalusd = amtbitcoin * HBPU

    fee = finalusd * 0.002

    fee = ceil(fee * 10000) / 10000.0
    if fee <= 0.0001:
        fee = 0.0001

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade('btc_usd', 'buy', float(btcusdasks[0][0]), maxv)

            y = trader.trade('btc_eur', 'sell', float(btceurbids[0][0]), amtlitecoin)

            x = trader.trade('eur_usd', 'sell', float(eurusdbids[0][0]), amtbitcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

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

                trader.trade('btc_usd', 'sell', float(btcusdbids[0][0]), amtlitecoin)

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

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcbtc"
    pair3 = "nvcbtc"
    pair4 = "nvcusd"

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

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

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "btcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg tried to go through a trade but it got cancled my homes' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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
                      message='yo dawg i did a trade homes' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "btcusd"
    pair2 = "btceur"
    pair3 = "ltceur"
    pair4 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you tried to make some trades but hte got canceled my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg you tried to make some trades but hte got canceled my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ppcusd"
    pair2 = "ppcbtc"
    pair3 = "ltcbtc"
    pair4 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you cancedl a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg you cancedl a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie ' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "nvcusd"
    pair2 = "nvcbtc"
    pair3 = "ltcbtc"
    pair4 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I cnacled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I cnacled a trade ' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcbtc"
    pair3 = "ppcbtc"
    pair4 = "ppcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3 yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "nvcusd"
    pair2 = "nvcbtc"
    pair3 = "ppcbtc"
    pair4 = "ppcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie ' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie ' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ppcusd"
    pair2 = "ppcbtc"
    pair3 = "nvcbtc"
    pair4 = "nvcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade homie ' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg you canceld a trade homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "btcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "ltcrur"
    pair4 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld at rade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg I canceld at trade ' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "ltcrur"
    pair4 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceled a trade ' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3-yo dawg I canceled a trade' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "eurrur"
    pair4 = "eurusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "eurrur"
    pair4 = "eurusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_2(pair1, pair2, pair3, pair4)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair4[:3].upper(), amtnvccoin, pair4[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'sell', float(eval(pair4 + 'bids[0][0]')), amtnvccoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg you canceld a trade my homie ' + pair1 + pair2 + pair3 + pair4,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie ' + pair1 + pair2 + pair3 + pair4,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "eurrur"
    pair4 = "btceur"
    pair5 = "btcusd"

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg you canceld a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg you canceld a trade my homie ' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "btcusd"
    pair2 = "btcrur"
    pair3 = "eurrur"
    pair4 = "ltceur"
    pair5 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg a trade got canceled ' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg you made a trade my homie' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "btcrur"
    pair4 = "ltcbtc"
    pair5 = "ltcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg a trade got canceled' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg I canceld a trade ' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg I canceld a trade ' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg I canceld a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "eurusd"
    pair2 = "eurrur"
    pair3 = "btcrur"
    pair4 = "ppcbtc"
    pair5 = "ppcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg I caneled a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltcrur"
    pair3 = "btcrur"
    pair4 = "nvcbtc"
    pair5 = "nvcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3yo dawg I canceld the trade ' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='4 yo dawg I made some trazdes' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()

    pair1 = "ltcusd"
    pair2 = "ltceur"
    pair3 = "btceur"
    pair4 = "nvcbtc"
    pair5 = "nvcusd"

    starting_money = current_usd

    maxv = get_lowest_volume_for_strat_9(pair1, pair2, pair3, pair4, pair5)

    cost = float(eval(pair1 + 'asks[0][0]')) * maxv

    fee = calculate_fee(maxv)

    amtlitecoin = maxv - fee

    amtbitcoin = return_equivalent(pair2[:3].upper(), amtlitecoin, pair2[3:].upper())

    fee = calculate_fee(amtbitcoin)

    amtbitcoin -= fee

    amtnvccoin = return_equivalent(pair3[3:].upper(), amtbitcoin, pair3[:3].upper())

    fee = calculate_fee(amtnvccoin)

    amtnvccoin -= fee

    amtdickcoin = return_equivalent(pair4[3:].upper(), amtnvccoin, pair4[:3].upper())

    fee = calculate_fee(amtdickcoin)

    amtnvccoin -= fee

    finalusd = return_equivalent(pair5[:3].upper(), amtdickcoin, pair5[3:].upper())

    fee = calculate_fee(finalusd)

    finalusd -= fee

    if finalusd > cost:
        def do_trade():


            z = trader.trade(pair1[:3] + '_' + pair1[3:], 'buy', float(eval(pair1 + 'asks[0][0]')), maxv)

            y = trader.trade(pair2[:3] + '_' + pair2[3:], 'sell', float(eval(pair2 + 'bids[0][0]')), amtlitecoin)

            x = trader.trade(pair3[:3] + '_' + pair3[3:], 'buy', float(eval(pair3 + 'asks[0][0]')),
                             amtbitcoin / float(eval(pair3 + 'asks[0][0]')))

            w = trader.trade(pair4[:3] + '_' + pair4[3:], 'buy', float(eval(pair4 + 'asks[0][0]')),
                             amtnvccoin / float(eval(pair4 + 'asks[0][0]')))

            v = trader.trade(pair5[:3] + '_' + pair5[3:], 'sell', float(eval(pair5 + 'bids[0][0]')), amtdickcoin)

            if z.received == 0:
                trader.cancelOrder(z.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if y.received == 0:
                trader.cancelOrder(y.order_id)

                trader.trade(pair1[:3] + '_' + pair1[3:], 'sell', float(eval(pair1 + 'bids[0][0]')), amtlitecoin)

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

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='3o dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            if w.received == 0:
                trader.cancelOrder(w.order_id)

                sendemail(from_addr='shemer77@gmail.com',
                          to_addr_list=['shemer77@gmail.com'],
                          cc_addr_list='',
                          subject=thisname,
                          message='4yo dawg I canceld the trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                          login='shemer77',
                          password='augedqrdvoplyqjm')
                return

            sendemail(from_addr='shemer77@gmail.com',
                      to_addr_list=['shemer77@gmail.com'],
                      cc_addr_list='',
                      subject=thisname,
                      message='yo dawg I made a trade' + pair1 + pair2 + pair3 + pair4 + pair5,
                      login='shemer77',
                      password='augedqrdvoplyqjm')

        do_trade()


def intiliaze_trader():
    global trader
    handler = btceapi.KeyHandler(key_file, resaveOnDeletion=True)

    trader = btceapi.TradeAPI(handler.keys[0], handler)


intiliaze_trader()
get_current_usd()

strategyone()
