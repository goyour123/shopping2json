import re
import requests

def get_shopid_by_username(username):
    """ Use the user account to get shop id from the website.
    Return the shop id.
    """

    url_shopid = 'https://shopee.tw/api/v1/shop_ids_by_username/'
    payload = {
        "usernames": [username]
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer': 'https://shopee.tw/' + username,
        'x-csrftoken': 'T8C6PYl7ZrCuXyvcfAKeprt8CqJLMXBO',
        'Cookie': '_ga=GA1.2.738446604.1499652300; \
                   SPC_F=oVPCZKPQJJiAzww4hPS3IelVSDl7uiv6; \
                   SPC_EC="a/oyTT0arvpDfihzs6yyqhAV7q0N9pwhWBt8dsj2KLSBpt1e1xaQTuJwkvcCgQK6BoEpWFdTKEiJayOhJzjTXPl70fZy+X6WIKakB80ObaX62w5gIrJQwyyYp51krpwxcELGWwJe9Jbz9PoMwq5ZGg=="; \
                   SPC_U=26130117; \
                   REC_T_ID=31c819ee-6514-11e7-b739-c81f66de8516; \
                   SPC_T_ID="OxYnOCBxqqgIxps6EXvkzV77fkV8M+oFxObdcBbG3VQqWuOMPZcvLWsFnv2nmrfQv7i7A5JNjQFU7hnyQAr1Cd4tL44xhcOoxZq+ee8n9g0="; \
                   SPC_T_IV="aseJ4vJALqpqtGVtYP94oQ=="; \
                   SPC_IA=-1; _gid=GA1.2.1310785758.1502469373; \
                   SPC_SI=8cdbxdtfjyztrgncb51ilxvwqptk91r6; \
                   SPC_SC_TK=288fc8a6053fe3268513cc76eaf5e4e8; \
                   SPC_SC_UD=26130117; \
                   csrftoken=T8C6PYl7ZrCuXyvcfAKeprt8CqJLMXBO; \
                   _gat=1'
    }
    resp = requests.post(url_shopid, json=payload, headers=headers)
    resp_json = resp.json()
    shop_id = resp_json[0][username]
    return str(shop_id)


def get_params(url):
    """Parse the full or shorter url to get params for item detail api url.
    Detect the different urls of product, full or shorter, and return the params for item detail
    api url.
    """
    url_type = re.search('http.*://shopee.tw/(.*?)/[0-9]*/', url).group(1)

    if url_type == 'product':
        shop_id, item_id = re.search('http.*://shopee.tw/product/([0-9]*?)/([0-9]*?)/', url).group(1, 2)
    else:
        account, item_id = re.search('http.*://shopee.tw/(.*)/([0-9]*)/', url).group(1, 2)
        shop_id = get_shopid_by_username(account)

    params = {
        'item_id': item_id,
        'shop_id': shop_id
    }
    return params

headers = {
    'Host': 'shopee.tw',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'if-none-match-': '*',
}

PRODUCT_SHORTER = 'https://shopee.tw/goyour123/737121539/'
PRODUCT_URL = 'https://shopee.tw/product/26128781/393544259/'

ITEM_DETAIL_API_URL = 'https://shopee.tw/api/v1/item_detail/'

res = requests.get(ITEM_DETAIL_API_URL, params=get_params(PRODUCT_SHORTER), headers=headers)
json = res.json()

print('HTTP Status Code: ' + str(res.status_code))
print (json['name'])
print (json['price'])
