from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AccountSerializer, FavouriteSerializer
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
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        favouritePlaces = Favourite.objects.filter(user=pk)
        serializer = FavouriteSerializer(favouritePlaces, many=True)
        return Response(serializer.data)