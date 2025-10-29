from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_open, name='news_open'),
    path('news/create/', views.news_create, name='news_create'),
]