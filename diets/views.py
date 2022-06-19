from django.shortcuts import render
from django.http import HttpResponseServerError


import requests
import re
# Create your views here.

# TODO static daily diets
# TODO Users preferences

api_keys = ["41fec56909474683a86fdcfa31c0f9d7",
            "717a16dc5e4f4d50b4a5ad4eaf0ca926",
            "62620d0fc94a4c5ba408be5e84fc9a8a",
            "32ae301b8fe4468a9b2629ee0cacd81f",
            "b08783f666474784987be694525efb82"
            ]

def diet(request):
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'})
    tags = ["breakfast", "brunch", "lunch", "dinner"]
    response = {'recipes': []}
    for tag in tags:
        url = f'https://api.spoonacular.com/recipes/random?apiKey=APIKEY&number=1&tag={tag},healthy'
        for ak in api_keys:
            url = url.replace("APIKEY", ak)
            temp = session.get(url=url)
            if temp.status_code == 200:
                break 
            else:
                url = url.replace(ak,"APIKEY")
        if temp.status_code != 200:
            return HttpResponseServerError()
        temp = temp.json()
        temp['recipes'][0]['tag'] = tag
        response['recipes'].extend(temp['recipes'])
    return render(request, 'diets/diet.html', {'response': response, "tags": tags})

# TODO validate id


def detail(request, id):
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'})
    url = f'https://api.spoonacular.com/recipes/{id}/information?apiKey=APIKEY'
    for ak in api_keys:
        url = url.replace("APIKEY", ak)
        response = session.get(url=url).json()
        if response.status_code == 200:
            break 
        else:
            url = url.replace(ak,"APIKEY")
    if response.status_code != 200:
        return HttpResponseServerError()
    response['protein'] = re.findall(
        r'\d{1,}g of protein', response['summary'])[0].split()[0]
    response['fat'] = re.findall(r'\d{1,}g of fat', response['summary'])[
        0].split()[0]
    response['calories'] = re.findall(
        r'\d{1,} calories', response['summary'])[0].split()[0]
    return render(request, 'main/detail.html', {'response': response})
