from django.urls import path
from cart import views
app_name='cart'
urlpatterns = [
    path('cart/', views.Cart),
    path('update/<int:gid>/', views.CartUpdateView.as_view()),
    path('delete/<int:gid>/', views.CartDeleteView.as_view()),
    path('perinf/', views.perInf),
]