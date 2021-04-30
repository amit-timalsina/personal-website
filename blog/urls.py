from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='posts'),

    #CRUD PATHS
    path('create_post/', views.createPost, name='create_post'),
    path('update_post/<slug:slug>/', views.updatePost, name='update_post'),
    path('delete_post/<slug:slug>/', views.deletePost, name='delete_post'),
]