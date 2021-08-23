from django.conf.urls import url
from user import views
from django.contrib import admin
from django.urls import path
from user import views
app_name='user'
urlpatterns = [
    path('login/', views.Login,name='login'),
    path('register/',views.Register,name='register'),
    path('perInf/',views.perInf),
    path('logout/',views.Logout),
]