from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import Rrgistrionsiralizer, Profilesiralizer, PasswordSirializer, CustomUserWithBlogsSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import CustomUser, Blogs
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        print(request.data)
        serializer = Rrgistrionsiralizer(data=request.data)
        if serializer.is_valid():
            newuser = serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            # Use get() to avoid KeyError if 'refresh' is missing
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Token successfully blacklisted."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": {"Token is not given"}}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            # Convert TokenError to a string or extract a meaningful message
            # Convert the TokenError instance to a string
            error_message = str(e)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred while processing the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class profileUser(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = Profilesiralizer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileImage(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request):
        user = request.user
        serializer = PasswordSirializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileFatch(generics.RetrieveAPIView):
    def get(self, request):
        user = request.user
        serializer = Profilesiralizer(user)
        return Response(serializer.data)



class Getblogs(generics.ListAPIView):
    queryset = Blogs.objects.all().order_by('-id')
    serializer_class = CustomUserWithBlogsSerializer
    # permission_classes=[permissions.IsAuthenticated]
