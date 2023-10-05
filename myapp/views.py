from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import Rrgistrionsiralizer, Profilesiralizer, ImageSirializer, CustomUserWithBlogsSerializer, Blogsiralizer
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
        serializer = ImageSirializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileFatch(generics.RetrieveAPIView):
    def get(self, request):
        user = request.user
        serializer = Profilesiralizer(user)
        return Response(serializer.data)


class UploadBlog(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Blogsiralizer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        data['username'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post Upload successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistroyBlog(generics.DestroyAPIView):
    def delete(self, request, id):
        try:
            data = get_object_or_404(Blogs, id=id)
            if data.username == request.user:
                data.delete()
                return Response({'message': 'Post Delete Successful'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': 'Post Not Found'}, status=status.HTTP_400_BAD_REQUEST)


class Getblogs(generics.ListAPIView):
    queryset = Blogs.objects.all().order_by('-id')
    serializer_class = CustomUserWithBlogsSerializer
    permission_classes = [permissions.IsAuthenticated]


class getProfileWithBlog(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserWithBlogsSerializer

    def get_queryset(self):
        username = self.request.user
        queryset = Blogs.objects.filter(username=username)
        return queryset


class getOtherProfileWithBlog(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserWithBlogsSerializer

    def get_queryset(self):
        id = self.kwargs['username']
        username = get_object_or_404(CustomUser, username=id)
        print(username.username)
        queryset = Blogs.objects.filter(username=username.id)
        return queryset


class DeleteProfile(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = get_object_or_404(CustomUser, email=request.user)
        if user:
            user.delete()
            return Response({"message": "user Delete Successful"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "user not found"}, status=status.HTTP_204_NO_CONTENT)

class AddandRemoveLike(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request,id):
        user_id=request.user.id
        user_name=request.user
        obj=get_object_or_404(Blogs,id=id)
        if obj:
            print(obj.likes.all())
            if user_name in obj.likes.all():
                obj.likes.remove(user_id)
                return Response({'message': f'You disliked {obj.title}.'}, status=status.HTTP_200_OK)
            else:
                obj.likes.add(user_id)
                return Response({'message': f'You liked  {obj.title}'}, status=status.HTTP_201_CREATED)    
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
