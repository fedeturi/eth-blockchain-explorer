from typing import Optional
from fastapi import FastAPI
import time
from typing import Mapping
import requests
from pprint import pprint
import calendar
import datetime

from requests.models import HTTPError

app = FastAPI()


@app.get("/blocks-count")
async def get_latest_block():
    
    URL = "https://api.etherscan.io/api"
    HEADERS = {
        'accept': 'application/json'
    }

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    QUERYSET = {
        'module': 'block',
        'action': 'getblocknobytime',
        'timestamp': str(utc_time),
        'closest': 'before',
        'apikey': '4A824VS77HUTKMPJ6PUQPHIDUZPHMP2AHQ',
    }

    response = requests.get(URL, headers=HEADERS, params=QUERYSET)

    if response.status_code == 200:
        latest_block_num = response.json().get('result')
        return latest_block_num
    else:
        return "TODO error"


@app.get("/block-info/{block_num}")
async def get_block_info(block_num):
    URL = "https://api.etherscan.io/api"

    HEADERS = {
        'accept': 'application/json'
    }

    QUERYSET = {
        'module': 'proxy',
        'action': 'eth_getBlockByNumber',
        'tag': hex(int(block_num)),
        'boolean': 'true',
        'apikey': '4A824VS77HUTKMPJ6PUQPHIDUZPHMP2AHQ',
    }
        
    response = requests.get(URL, headers=HEADERS, params=QUERYSET)

    if response.status_code == 200:
        full_block_info = response.json()
        return full_block_info.get('result')
    else:
        pass


@app.get("/address-tx-hist/{address}")
async def get_address_tx_hist(address):
    URL = "https://api.etherscan.io/api"
    HEADERS = {
        'accept': 'application/json'
    }

    latest_block = get_latest_block()

    QUERYSET = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': '0',
        'endblock': latest_block,
        'page': '1',
        'offset': '10',
        'sort': 'asc',
        'apikey': '4A824VS77HUTKMPJ6PUQPHIDUZPHMP2AHQ',
    }
        
    response = requests.get(URL, headers=HEADERS, params=QUERYSET)

    if response.status_code == 200:
        address_tx_list_result = response.json()
        return address_tx_list_result.get('result')
    else:
        pass