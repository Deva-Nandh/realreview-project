from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.image_list_create, name='image-list-create'),
]
