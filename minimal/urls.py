from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('like/', views.like, name='like'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('user_detail/<int:pk>', views.user_detail, name='user_detail'),
    path('user_update/<int:pk>', views.user_update, name='user_update'),
    path('user_posts/<int:pk>', views.user_posts, name='user_posts'),
    path('user_posts/satisfied/<int:pk>', views.user_posts_satisfied, name='user_posts_satisfied'),
    path('user_posts/planed/<int:pk>', views.user_posts_planed, name='user_posts_planed'),
    path('user_posts/threw/<int:pk>', views.user_posts_threw, name='user_posts_threw'),   
]