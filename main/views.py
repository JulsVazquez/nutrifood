from tkinter import EXCEPTION
from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseServerError

import requests

api_keys = ["41fec56909474683a86fdcfa31c0f9d7",
            "717a16dc5e4f4d50b4a5ad4eaf0ca926",
            "62620d0fc94a4c5ba408be5e84fc9a8a",
            "32ae301b8fe4468a9b2629ee0cacd81f",
            "b08783f666474784987be694525efb82"
            ]

def home(request):
    total_recipes = Recipe.objects.all().count()
    context = {
        "title": "Homepage",
        "total_recipes": total_recipes,
    }

    return render(request, "main/home.html", context)


def search(request):
    tag = ""
    search = ""
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'})
    if "search" in request.GET:
        search = request.GET.get("search")

    if request.GET.get("breakfast"):
        tag = "breakfast"
    elif request.GET.get("appetizers"):
        tag = "appetizers"
    elif request.GET.get("lunch"):
        tag = "lunch"
    elif request.GET.get("salads"):
        tag = "salads"
    elif request.GET.get("dinner"):
        tag = "dinner"
    elif request.GET.get("dessert"):
        tag = "dessert"
    elif request.GET.get("vegan"):
        tag = "vegan"
    elif request.GET.get("vegetarian"):
        tag = "vegetarian"

    response = ""
    if search and tag:
        print("s and t")
        url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey=APIKEY&number=6&query={search}&tag={tag}'
    elif search and not tag:
        print("s")
        url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey=APIKEY&number=6&query={search}'
    elif not search and tag:
        print("t")
        url = f'https://api.spoonacular.com/recipes/random?apiKey=APIKEY&number=6&tag={tag}'
    else:
        print("ninguno")
        url = f'https://api.spoonacular.com/recipes/random?apiKey=APIKEY&number=6'
    print(url)
    for ak in api_keys:
        url = url.replace("APIKEY", ak)
        response = session.get(url=url)
        if response.status_code == 200:
            break 
        else:
            url = url.replace(ak,"APIKEY")
    if response.status_code != 200:
        return HttpResponseServerError()
    response = response.json()
    if 'recipes' in response:
        total = len(response['recipes'])
        response = response['recipes']
    if 'results' in response:
        total = len(response['results'])
        response = response['results']
    # else:
    #     total = 1

    context = {
        "tag": tag,
        "total": total,
        "response": response,
    }
    return render(request, "main/search.html", context)
