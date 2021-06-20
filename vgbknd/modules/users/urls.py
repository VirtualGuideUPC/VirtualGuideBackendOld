from django.contrib.auth.models import User
from django.urls import path
from .views import AddFavourite, ListFavourite, RegisterView, LoginView, UserView, LogoutView 

urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/user/', UserView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/favourite/create', AddFavourite.as_view()),
    path('users/<str:pk>/favourites', ListFavourite.as_view())
]