from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import  get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserCreateSerializer,UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser



User = get_user_model()
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        data = request.data

        serializer =UserCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)
        return Response(user.data ,status=status.HTTP_201_CREATED)
    

class RetrieveUpdateDeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self,request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data,status=status.HTTP_200_OK)

    def put(self,request):
        user = request.user
        data = request.data

        print('Incoming PUT request data:', data)


        update_data = {
            'first_name': data.get('firstName', user.first_name),
            'last_name': data.get('lastName', user.last_name),
            'email': data.get('email', user.email),
        }

        serializer = UserSerializer(user, data=update_data, partial=True)

        if not serializer.is_valid():
            print('Serializer errors:', serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        print('Updated user data:', serializer.data)

        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def delete(self,request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
     

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
        token['isSuperuser'] = user.is_superuser
        
        return token



class ProfilePictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        user = request.user
        if not user.profile:
            return Response({"detail": "No profile picture found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"profile_picture_url": user.profile.url}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        print(request.data)
        profile_picture = request.FILES.get('profile')
        print(profile_picture)

        if not profile_picture:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        user.profile = profile_picture
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user.profile.delete()  # This deletes the file from the storage
        user.profile = None  # Optionally set the profile field to None
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
     

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer







class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_superuser=False) 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, pk=None):
        if pk is None:
            return Response({'detail': 'User ID is required for updating'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    def delete(self, request, pk=None):
        if pk is None:
            return Response({'detail': 'User ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    