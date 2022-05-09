from django.shortcuts import render

import requests
# Create your views here.


def index(request):
    response = requests.get(
        'https://api.edamam.com/api/nutrition-data?app_id=d13f79e4&app_key=1df679c70c7bacdbb4ea010b3b0d1676&nutrition-type=cooking&ingr=chiken').json()
    return render(request, 'index.html', {'response': response})
