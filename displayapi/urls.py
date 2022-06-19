from django.urls import path
from .views import IndexFormView
urlpatterns = [
    path('', IndexFormView.as_view()),
]
