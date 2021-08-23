from django.conf.urls import url
from user import views
from django.contrib import admin
from django.urls import path
from user import views
app_name='user'
urlpatterns = [
    path('login/', views.Login),
    path('register/',views.Register),
    path('perInf/',views.perInf)

]