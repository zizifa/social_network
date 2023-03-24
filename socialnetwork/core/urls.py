from django import urls
from .import views
from django.urls import path
urlpatterns=[
    path('',views.index , name='index'),
    path('setting/', views.setting, name='setting'),
    path('signup/',views.signup , name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),

]
