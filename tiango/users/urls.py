from django.conf.urls import url
from users import views
from django.contrib import admin
from django.urls import path
from users import views
app_name='user'
urlpatterns = [
    path('login/', views.Login),
    path('register/',views.Register),
    path('perInf/',views.perInf)

]
