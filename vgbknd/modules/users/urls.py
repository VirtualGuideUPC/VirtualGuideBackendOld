from django.contrib.auth.models import User
from django.urls import path
from .views import AddFavourite, AddCategoryPreference, AddTypePlacePreference, ListFavourite, ListFavouriteDepartment, ListPreference, RegisterView, LoginView, UpdateCategoryPreference, UpdateTypePlacePreference, UserView, LogoutView 

urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/user/', UserView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/favourite/create/', AddFavourite.as_view()),
    path('users/preference/category/create/', AddCategoryPreference.as_view()),
    path('users/preference/typeplace/create/', AddTypePlacePreference.as_view()),
    path('users/:pk/favourites/departments/', ListFavouriteDepartment.as_view()),
    path('users/:pk/favourites/departments/:id/', ListFavourite.as_view()),
    path('users/preferences/', ListPreference.as_view()),
    path('users/preference/category/update/', UpdateCategoryPreference.as_view()),
    path('users/preference/typeplace/update/', UpdateTypePlacePreference.as_view())
]