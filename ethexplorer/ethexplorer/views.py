from django.db.models import base
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from typing import Optional
import time
from typing import Mapping
import requests
from pprint import pprint
import calendar
import datetime
import brownie

from requests.api import get


def get_latest_block():

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
        pass


def get_block_info(block_num):
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
        return full_block_info
    else:
        pass


def get_address_tx_hist(address):
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
        if address_tx_list_result.get('message') == 'OK':
            return address_tx_list_result.get('result')
    else:
        return None


def get_eth_price():
    URL = "https://api.etherscan.io/api"
    HEADERS = {
        'accept': 'application/json'
    }

    QUERYSET = {
        'module': 'stats',
        'action': 'ethprice',
        'apikey': '4A824VS77HUTKMPJ6PUQPHIDUZPHMP2AHQ',
    }

    response = requests.get(URL, headers=HEADERS, params=QUERYSET)

    if response.status_code == 200:
        prices = response.json()
        if prices.get('message') == 'OK':
            eth_usd = prices.get('result').get('ethusd')
            eth_btc = prices.get('result').get('ethbtc')
            return eth_usd, eth_btc
    else:
        return None, None


def index(request):

    latest_mined_block = int(get_latest_block())
    latest_mined_block_str = '{0:,d}'.format(latest_mined_block)
    block_info = get_block_info(latest_mined_block).get('result')
    block_tx_list = block_info.get('transactions')
            
    for tx in block_tx_list:
        tx['value'] = int(tx.get('value'), base=16)
    miner = block_info.get('miner')
    difficulty = '{0:,d}'.format(int(block_info.get('difficulty'), base=16))

    tx_count = len(block_tx_list)
    tx_list = []
    eth_usd, eth_btc = get_eth_price()
    address = ''
    address_tx_count = 0

    try:
        if request.method == 'POST':
            address = request.POST.get('address')
            tx_list = get_address_tx_hist(address)
            address_tx_count = len(tx_list)
        else:
            raise ValueError()
    except Exception as e:
        print(e)

    return render(request, 'index.html', {
        'title': 'ETH Blockchain Explorer',
        'cover_header': 'ETH Blockchain Explorer',
        'cover_body': 'Explore the ETHEREUM Blockchain with this tool, using enhanced capabilities provided by ',
        'main_cta': "Let's Go!",
        'home': 'Home',
        'stats': 'Latest Block Statistics',
        'stats_body': 'Latests mined block information and transactions list',
        'block_tx_list': block_tx_list,
        'searched_address': address,
        'address_tx_list': tx_list,
        'address_tx_count': address_tx_count,
        'explorer': 'Address Explorer',
        'explorer_body': 'Search by Address to see more details about its transactions. ',
        'latest_mined_block': latest_mined_block_str,
        'miner': miner,
        'difficulty': difficulty,
        'latst_block_tx_count': tx_count,
        'search': 'Explore',
        'address_error': 'Invalid Address. Please check it and try again.',
        'eth_usd': eth_usd,
        'eth_btc': eth_btc
    })


def address_details(request):
    pass
