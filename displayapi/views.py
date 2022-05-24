from ast import Index
from django.shortcuts import render
from django.views.generic.edit import FormView

import requests

from .forms import IndexForm
# Create your views here.


class IndexFormView(FormView):
    form_class = IndexForm
    template_name = "index.html"

    def post(self, request):
        form = IndexForm(data = request.POST)
        if form.is_valid():
            ingredient = form.cleaned_data["ingredient"]
            response = self.get_request(ingredient)
            form = IndexForm()
            print(response)
            return render(request, 'index.html', {'response' : response, 'ingredient': ingredient.upper, 'form':form})
        return render(request, 'index.html')
        
    def get_request(self, ingredient):
        response = requests.get(
        f'https://api.edamam.com/api/nutrition-data?app_id=d13f79e4&app_key=1df679c70c7bacdbb4ea010b3b0d1676&nutrition-type=logging&ingr={ingredient}').json()
        return response
        

