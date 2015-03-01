import requests

headers = {
'Cookie': 'steamLogin=76561197990722385%7C%7C6BA676C5F24DD18768CF1BCB12F4FDE1DF88C93D; sessionid=NDI4NDU1NzQz; Steam_Language=english; steamCC_98_224_169_23=US; timezoneOffset=-18000,0; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A12%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D',
'Referer': 'http://steamcommunity.com/market/listings/753/219150-Burn%20%28Trading%20Card%29'}
r5 = requests.post('http://steamcommunity.com/market/buylisting/2854459923441547648', headers=headers, verify=False)