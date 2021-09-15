from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {
        'title': 'ETH Blockchain Explorer',
        'cover_header': 'ETH Blockchain Explorer',
        'cover_body': 'Explore the ETHEREUM Blockchain with this tool, using enhanced capabilities provided by ',
        'main_cta': "Let's Go!",
        'home': 'Home',
        'stats': 'Stats',
        'explorer': 'Explorer',
        'mined_blocks': '124351',
        'block_tx_list': [
            '0x92362d3c00a7d4ff442ee416b59b2222d6b9c4c37d5d314ac96a8dbf77d05b17',
            '0x92362d3c00a7d4ff442ee416b59b2222d6b9c4c37d5d314ac96a8dbf77d05b17',
            '0x92362d3c00a7d4ff442ee416b59b2222d6b9c4c37d5d314ac96a8dbf77d05b17',
            '0x92362d3c00a7d4ff442ee416b59b2222d6b9c4c37d5d314ac96a8dbf77d05b17',
            '0x92362d3c00a7d4ff442ee416b59b2222d6b9c4c37d5d314ac96a8dbf77d05b17'
        ]
    })