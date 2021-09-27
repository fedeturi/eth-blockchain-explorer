from urllib import request
from pprint import pprint

url = 'http://localhost:8000'

response = request.urlopen(url)
pprint(response.read())