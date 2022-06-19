from django.urls import path
from .views import diet,detail
urlpatterns = [
    path("mydiet", diet, name="mydiet"),
    path("detail/<int:id>",detail,name = "detail" )
]
