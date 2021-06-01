from django.urls import path
from .views import TouristicPlaceById, TouristicPlaceListView, CreateTouristicPlace, PictureTouristicPlaceListView, CreatePictureTouristicPlace

urlpatterns = [
    path('places/create/', CreateTouristicPlace.as_view()),
    path('places/list/', TouristicPlaceListView.as_view()),
    path('places/<str:pk>/', TouristicPlaceById.as_view()),
    path('places/createphotos/', CreatePictureTouristicPlace.as_view()),
    path('places/<str:pk>/photos/', PictureTouristicPlaceListView.as_view())
]