from rest_framework.views import APIView
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import *

# Create your views here.
class CreateReview(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ReviewTouristicPlaceListView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        reviews = Review.objects.filter(touristic_place=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

