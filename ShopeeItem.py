import re
import json
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
    'Accept': '*/*',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    # 'Referer': 'https://shopee.tw/%E5%9C%93%E7%9B%A4%E5%BC%8F%E8%AA%BF%E5%85%89%E5%99%A8%E5%BB%B6%E9%95%B7%E7%B7%9A-3M-i.26128781.737121539',
    'x-requested-with': 'XMLHttpRequest',
    'x-api-source': 'pc',
    'if-none-match-': '55b03-4e8849c5ab0a16b18a1cc1950c2c3d1d',
    'origin': 'https://shopee.tw',
    'Cookie': '_ga=GA1.2.1573711670.1520060862; _gac_UA-61915057-6=1.1520060869.Cj0KCQiAieTUBRCaARIsAHeLDCQYvSYw9HxGkx3kRaqahivcK8I4ozGM4Q41q4f7VVF0TJzp33GrnzsaAi-IEALw_wcB; cto_lwid=b831de58-2022-41e2-b78f-57884eed5b6c; SPC_IA=-1; SPC_EC=-; SPC_F=YzMNdR2qIQPVRP8UumDaMul4bCiHjKyO; REC_T_ID=908b8540-1eb1-11e8-a08e-c81f66de8516; SPC_T_ID="+l9S+x9IzIWFj7SAeqHU+eJ/s71Q//t1bVymAOcbBzwJX22rLBQNw6RfIYu+cbpI5Wcw4XRaQsHVdPbO2MiEgqPmfFDFI2P/I06OoX9OQvY="; SPC_U=-; SPC_T_IV="LbM8UNFvfR95ohEwb0taaA=="; __BWfp=c1520060864864x8aa629cb3; SPC_SI=yqupjdgkese4ge81qbge2174rzvb1fjq; _gid=GA1.2.155357059.1523712914; csrftoken=gyC0jkgbzv9Uhi3KOYvVe4qv2w5iov8h; SPC_SC_TK=; UYOMAPJWEMDGJ=; SPC_SC_UD=; _gat=1',
    'Connection': 'keep-alive'
}

PRODUCT_SHORTER = 'https://shopee.tw/goyour123/1072932847/'
PRODUCT_URL = 'https://shopee.tw/product/26128781/393544259/'

ITEM_DETAIL_API_URL = 'https://shopee.tw/api/v1/item_detail/'

res = requests.get(ITEM_DETAIL_API_URL, params=get_params(PRODUCT_SHORTER), headers=headers)
res_json = res.json()

print('HTTP Status Code: ' + str(res.status_code))

item_dict = {
    'Name': res_json['name'],
    'Price': int(res_json['price'])
}

item_json = json.JSONEncoder().encode(item_dict)

with open('item.json', 'w') as file_json:
    file_json.write(item_json)

