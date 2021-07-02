from django.contrib.auth.models import User
from django.urls import path
from .views import AddFavourite, AddCategoryPreference, AddTypePlacePreference, ListFavourite, ListPreference, RegisterView, LoginView, UserView, LogoutView 

urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/user/', UserView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/favourite/create/', AddFavourite.as_view()),
    path('users/preference/category/create/', AddCategoryPreference.as_view()),
    path('users/preference/typeplace/create/', AddTypePlacePreference.as_view()),
    path('users/favourites/', ListFavourite.as_view()),
    path('users/preferences/', ListPreference.as_view())
]