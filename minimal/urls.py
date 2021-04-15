from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('user_detail/<int:pk>', views.user_detail, name='user_detail'),
]