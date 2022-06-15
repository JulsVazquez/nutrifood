from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    total_recipes = Recipe.objects.all().count()
    context = {
        "title": "Homepage",
        "total_recipes": total_recipes,
    }

    return render(request, "main/home.html", context)


def search(request):
    recipes = Recipe.objects.all()

    if "search" in request.GET:
        query = request.GET.get("search")
        queryset = recipes.filter(Q(title__icontains=query))

    if request.GET.get("breakfast"):
        results = queryset.filter(Q(topic__title__icontains="breakfast"))
        topic = "breakfast"
    elif request.GET.get("appetizers"):
        results = queryset.filter(Q(topic__title__icontains="appetizers"))
        topic = "appetizers"
    elif request.GET.get("lunch"):
        results = queryset.filter(Q(topic__title__icontains="lunch"))
        topic = "lunch"
    elif request.GET.get("salads"):
        results = queryset.filter(Q(topic__title__icontains="salads"))
        topic = "salads"
    elif request.GET.get("dinner"):
        results = queryset.filter(Q(topic__title__icontains="dinner"))
        topic = "dinner"
    elif request.GET.get("dessert"):
        results = queryset.filter(Q(topic__title__icontains="dessert"))
        topic = "dessert"
    elif request.GET.get("vegan"):
        results = queryset.filter(Q(topic__title__icontains="vegan"))
        topic = "vegan"
    elif request.GET.get("vegetarian"):
        results = queryset.filter(Q(topic__title__icontains="vegetarian"))
        topic = "vegetarian"

    total = results.count()

    # paginate results
    paginator = Paginator(results, 3)
    page = request.GET.get("page")
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {
        "topic": topic,
        "page": page,
        "total": total,
        "query": query,
        "results": results,
    }
    return render(request, "main/search.html", context)


def detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    context = {
        "recipe": recipe,
    }
    return render(request, "main/detail.html", context)
