from modules.places.serializers import DepartmentSerializer
from django.http import response
from modules.places.models import Province, Department, TouristicPlace
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegisterAccountSerializer, AccountSerializer, FavouriteSerializer, FavouriteTpSerializer, PreferenceCategorySerializer, PreferenceTypePlaceSerializer, PreferenceSubCategorySerializer
from .models import *
import jwt   
import datetime
from rest_framework import status

# Create your views here.

class RegisterView(APIView):
    def post(self, request):

        typeplaces=request.data.pop('type_place')
        categories= request.data.pop('category')
        subcategories=request.data.pop('subcategory')

        email=request.data['email']
        serializer=AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
        if(serializer.is_valid()):

            accounts= Account.objects.all()
            serializer=RegisterAccountSerializer(accounts, many=True)
            for dicts in serializer.data:
                if dicts['email']==email:
                    accountId=dicts['account_id']

            for tp in typeplaces:
                tpserializer=PreferenceTypePlaceSerializer(data={"type_place": tp, "user": accountId, "status":False})
                tpserializer.is_valid(raise_exception=True)
                tpserializer.save()
        
            for cat in categories:
                catserializer=PreferenceCategorySerializer(data={"category": cat, "user": accountId, "status":False})
                catserializer.is_valid(raise_exception=True)
                catserializer.save()        
        
            for subcat in subcategories:
                subcatserializer=PreferenceSubCategorySerializer(data={"subcategory": subcat, "user":accountId, "status":False})
                subcatserializer.is_valid(raise_exception=True)
                subcatserializer.save()      


        return Response(subcatserializer.data) 
        
class ListPreferedTypePlace(APIView): 

    def get(self, request):

        preferedTypePlaces= PreferenceTypePlace.objects.all()
        serializer=PreferenceTypePlaceSerializer(preferedTypePlaces, many=True)
        return Response(serializer.data)

class ListPreferedCategory(APIView): 

    def get(self, request):

        preferedCategories= PreferenceCategory.objects.all()
        serializer=PreferenceCategorySerializer(preferedCategories, many=True)
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

class ListFavouriteDepartment(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        favouritePlaces = Favourite.objects.filter(user=pk).values_list('touristic_place', flat=True)
        
        id_list = []
        
        for e in favouritePlaces:
            id_list.append(e)

        tp = TouristicPlace.objects.filter(touristicplace_id__in=id_list).values_list('province', flat=True)

        province_list = []

        for p in tp:
            province_list.append(p)

        provinces = Province.objects.filter(province_id__in=province_list).values_list('department', flat=True)

        department_list = []
        
        for d in provinces:
            department_list.append(d)

        print("DL: ", department_list)

        departments = Department.objects.filter(department_id__in=department_list)

        print("Depart: ", departments)

        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class ListFavourite(APIView):
    def get(self, request, pk, pk2):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        favouritePlaces = Favourite.objects.filter(user=pk, touristic_place__province__department=pk2)

        serializer = FavouriteTpSerializer(favouritePlaces, many=True)
        return Response(serializer.data)


class ListPreference(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        prcategory = PreferenceCategory.objects.filter(user=pk, status=True)

        catserializer = PreferenceCategorySerializer(prcategory, many=True)

        prsubcategory = PreferenceSubCategory.objects.filter(user=pk, status=True)

        subcatserializer = PreferenceSubCategorySerializer(prsubcategory, many=True)

        prtypeplace = PreferenceTypePlace.objects.filter(user=pk, status=True)

        tpserializer = PreferenceTypePlaceSerializer(prtypeplace, many=True)
        response = Response()

        response.data = {
            'categories': catserializer.data,
            'typeplaces': tpserializer.data,
            'subcategories': subcatserializer.data,
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
        serializer = PreferenceCategorySerializer(prtypeplace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTypePlacePreference(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['user']
        tp = request.data['type_place']
        prtypeplace = PreferenceTypePlace.objects.filter(user=user_id, type_place=tp).first()
        serializer = PreferenceTypePlaceSerializer(prtypeplace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountListView(APIView):
    def get(self, request):

        accounts= Account.objects.all()
        serializer=RegisterAccountSerializer(accounts, many=True)
        return Response(serializer.data)
