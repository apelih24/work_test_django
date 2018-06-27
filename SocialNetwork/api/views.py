from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import get_object_or_404

from SocialNetwork.models import Post

from .serializers import (
    PostSerializer,
    UserCreateSerializer,
    UserLogInSerializer,
    PostLikesSerializer
)
from .permition import IsOwnerOrReadOnly


class PostAPIView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()


class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class LogInUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLogInSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLogInSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            user = authenticate(username=new_data['username'], password=new_data['password'])
            login(request, user)
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostLikesSerializer(post)
    if request.method == 'GET':
        return Response(serializer.data, status=HTTP_200_OK)
    if request.method == 'POST':
        post.likes += 1
        post.save()
        return Response(serializer.data, status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostLikesSerializer(post)
    if request.method == 'GET':
        return Response(serializer.data, status=HTTP_200_OK)
    if request.method == 'POST':
        if post.likes > 0:
            post.likes -= 1
            post.save()
        return Response(serializer.data, status=HTTP_202_ACCEPTED)
