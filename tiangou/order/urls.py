from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from django.urls import reverse
from order import views
app_name='order'

urlpatterns = [
    
    path('placeorder/<int:gid>/',views.placeorder),
    path('payorder/<int:oid>/',views.payorder),
    path('logistics/',views.showlogistics),

]