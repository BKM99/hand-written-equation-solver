from django.urls import path

from . import views

urlpatterns = [
    path('api', views.home_view, name='home'),
    path('api/data', views.data_view, name='data'),
]
