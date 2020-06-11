from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('names/<names>', views.generate_names, name='generate_names')
]
