from django.urls import path

from . import views

app_name = 'socialnetwork'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.PostInfoView.as_view(), name='post_info')
]
