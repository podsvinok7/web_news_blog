from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
