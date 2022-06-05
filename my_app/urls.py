
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gadgets', views.gadgets, name='gadgets'),
    path('clothing', views.clothing, name='clothing'),
    path('other', views.other, name='other'),
]
