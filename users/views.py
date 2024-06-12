from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import  get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserCreateSerializer,UserSerializer


User = get_user_model()
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        data = request.data

        serializer =UserCreateSerializer(data=data)

        if not serializer.is_valid():
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)
        return Response(user.data ,status=status.HTTP_201_CREATED)
    

class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self,request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data,status=status.HTTP_200_OK)
    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
     """
    Custom token serializer to include additional user information in the token.
    """
     
     @classmethod
     def get_token(cls, user) -> Token:
        token = super().get_token(user)
     
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        
        return token
     

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer