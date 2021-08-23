from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from django.urls import reverse
from good import views
app_name='good'
urlpatterns = [
    
    path('list/<int:tid>/<int:num>/', views.list), #传递参数tid,num给函数list
    path('detail/<int:gid>/',views.detail), #同理
    

]