from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_open, name='news_open'),
    path('news/create/', views.news_create, name='news_create'),
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/category/<str:category>/', views.articles_list, name='articles_by_category'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('create-article/', views.create_article, name='create_article'),
    path('author/<int:user_id>/', views.author_articles, name='author_articles'),
    path('edit-article/<int:id>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete_article'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]