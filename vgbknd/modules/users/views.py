from django.http import response
from modules.places.models import Province
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AccountSerializer, FavouriteSerializer, PreferenceCategorySerializer, PreferenceTypePlaceSerializer, UpPreferenceCategorySerializer
from .models import *
import jwt   
import datetime

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AddCategoryPreference(APIView):
    def post(self, request):
        serializer = PreferenceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AddTypePlacePreference(APIView):
    def post(self, request):
        serializer = PreferenceTypePlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.account_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        print('payload', payload)

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        print('token', token)

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'id': user.account_id,
            'jwt': token
        }
        return response

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Account.objects.filter(account_id=payload['id']).first()
        serializer = AccountSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class AddFavourite(APIView):
    def post(self, request):
        serializer = FavouriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 

class ListFavourite(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = request.data['user']
        department_id = request.data['department']

        favouritePlaces = Favourite.objects.filter(user=user_id, touristic_place__province__department = department_id)

        serializer = FavouriteSerializer(favouritePlaces, many=True)
        return Response(serializer.data)


class ListPreference(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = request.data['user']

        prcategory = PreferenceCategory.objects.filter(user=user_id)

        catserializer = PreferenceCategorySerializer(prcategory, many=True)
        
        prtypeplace = PreferenceTypePlace.objects.filter(user=user_id)

        tpserializer = PreferenceTypePlaceSerializer(prtypeplace, many=True)
        response = Response()

        response.data = {
            'categories': catserializer.data,
            'typeplaces': tpserializer.data
        }
        return response

class ListTypePlacePreference(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['user']
        prtypeplace = PreferenceTypePlace.objects.filter(user=user_id)

        serializer = PreferenceTypePlaceSerializer(prtypeplace, many=True)
        return Response(serializer.data)

class UpdateCategoryPreference(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['user']
        cat = request.data['category']
        prtypeplace = PreferenceCategory.objects.filter(user=user_id, category=cat).first()
        print("Category: ", prtypeplace)
        serializer = PreferenceCategorySerializer(prtypeplace, data=request.data)
        serializer.save()
        return Response(serializer.data)