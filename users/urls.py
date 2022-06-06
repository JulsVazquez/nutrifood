from django.urls import path

from users.views import ProfileView

from allauth.account.decorators import login_required

urlpatterns = [
    path('profile/', login_required(ProfileView.as_view())),
]