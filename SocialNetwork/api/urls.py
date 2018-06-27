from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import (
    PostRUDView,
    PostAPIView,
    CreateUserView,
    LogInUserView,
    like_post,
    unlike_post
)

urlpatterns = [
    path('', PostAPIView.as_view()),
    path('<int:pk>/', PostRUDView.as_view()),
    path('like/<int:pk>/', like_post),
    path('unlike/<int:pk>/', unlike_post),
    path('signup/', CreateUserView.as_view()),
    path('login/', LogInUserView.as_view())
]
