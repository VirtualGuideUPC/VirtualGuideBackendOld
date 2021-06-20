from .services import PlaceService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import TouristicPlaceSerializer, PictureTouristicPlaceSerializer
from .models import *
import jwt

# Create your views here.

class CreateTouristicPlace(APIView):
    def post(self, request):
        serializer = TouristicPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TouristicPlaceListView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        touristicPlaces = TouristicPlace.objects.all()
        serializer = TouristicPlaceSerializer(touristicPlaces, many=True)
        return Response(serializer.data)

class TouristicPlaceById(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        touristicPlace = TouristicPlace.objects.filter(touristicplace_id=pk).first()
        province = Province.objects.filter(province_id=touristicPlace.province).first()
        #department = Department.objects.filter(department_id=province.department).first()
        #typePlace = TypePlace.objects.filter(typeplace_id=touristicPlace.type_place).first()
        response = Response()

        response.data = {
            'name': touristicPlace.name,
            'cost_info': touristicPlace.cost_info,
            'price': touristicPlace.price,
            'schedule_info': touristicPlace.schedule_info,
            'historic_info': touristicPlace.historic_info,
            'long_info': touristicPlace.long_info,
            'short_info': touristicPlace.short_info,
            'activities_info': touristicPlace.activities_info,
            'latitude': touristicPlace.latitude,
            'longitude': touristicPlace.longitude,
            'range': touristicPlace.tp_range
        }
        return response


class CreatePictureTouristicPlace(APIView):
   def post(self, request):
        serializer = PictureTouristicPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PictureTouristicPlaceListView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        pictureTouristicPlaces = PictureTouristicPlace.objects.filter(touristic_place=pk)
        serializer = PictureTouristicPlaceSerializer(pictureTouristicPlaces, many=True)
        return Response(serializer.data)

class NearbyPlaces(APIView):
    def post(self, request):
        touristicPlaces = TouristicPlace.objects.filter(type_place=1)
        print('tipo real: ', type(touristicPlaces))
        lat = request.data['latitude']
        lon = request.data['longitude']

        placeService = PlaceService(lat, lon) 
        
        tplist = placeService.tpnearbylist(touristicPlaces)
        
        serializer = TouristicPlaceSerializer(tplist, many=True)

        print('tipo final: ', type(serializer.data))

        return Response(serializer.data)