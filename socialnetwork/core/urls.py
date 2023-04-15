from django import urls
from .import views
from django.urls import path
urlpatterns=[
    path('',views.index , name='index'),
    path('setting/', views.setting, name='setting'),
    path('delete', views.delete, name='delete'),
    path('signup/',views.signup , name='signup'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('signin/', views.signin, name='signin'),
    path('search/', views.search, name='search'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('edit-post/', views.edit_post, name='edit-post'),
    #    path('likepost/<uuid:post_id>/', views.likepost, name='likepost'),
    path('likepost', views.likepost, name='likepost'),
    path('follower/', views.followercount, name='follower'),

]
