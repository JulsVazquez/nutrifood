from django.shortcuts import render

import requests
import re
# Create your views here.

# TODO static daily diets
# TODO Users preferences


def diet(request):
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'})
    tags = ["breakfast", "brunch", "lunch", "dinner"]
    response = {'recipes': []}
    for tag in tags:
        url = f'https://api.spoonacular.com/recipes/random?apiKey=717a16dc5e4f4d50b4a5ad4eaf0ca926&number=1&tag={tag},healthy'
        temp = session.get(url=url).json()
        temp['recipes'][0]['tag'] = tag
        response['recipes'].extend(temp['recipes'])
    return render(request, 'diets/diet.html', {'response': response, "tags": tags})

# TODO validate id


def detail(request, id):
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'})
    url = f'https://api.spoonacular.com/recipes/{id}/information?apiKey=717a16dc5e4f4d50b4a5ad4eaf0ca926'
    response = session.get(url=url).json()
    response['protein'] = re.findall(
        r'\d{1,}g of protein', response['summary'])[0].split()[0]
    response['fat'] = re.findall(r'\d{1,}g of fat', response['summary'])[
        0].split()[0]
    response['calories'] = re.findall(
        r'\d{1,} calories', response['summary'])[0].split()[0]
    return render(request, 'main/detail.html', {'response': response})
