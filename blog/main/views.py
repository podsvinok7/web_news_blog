from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FeedbackForm, NewsForm, ArticleForm, CommentForm
from .models import Feedback, News, Article
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'category', 'created_date', 'author']
        read_only_fields = ['id', 'created_date', 'author']
        
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['created_date', 'title']
    ordering = ['-created_date']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['created_date', 'title']
    ordering = ['-created_date']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def filter_by_category(self, request, category_name=None):
        articles = self.queryset.filter(category=category_name)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sort/(?P<sort_field>[^/.]+)')
    def sort_by_field(self, request, sort_field=None):
        if sort_field == 'date':
            articles = self.queryset.order_by('-created_date')
        else:
            articles = self.queryset.order_by(sort_field)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

def articles_list(request, category=None):
    if category:
        articles = Article.objects.filter(category=category)
        category_display = {
            'technology': 'Технологии',
            'science': 'Наука',
            'art': 'Искусство', 
            'sport': 'Спорт',
            'general': 'Общее'
        }
        current_category = category_display.get(category, category)
    else:
        articles = Article.objects.all()
        current_category = None
    
    articles = articles.order_by('-created_date')
    
    return render(request, 'main/author_articles.html', {
        'articles': articles,
        'current_category': current_category
    })


def author_articles(request, user_id):
    author = get_object_or_404(User, id=user_id)
    articles = Article.objects.filter(user=author)
    
    return render(request, 'main/author_articles.html', {
        'articles': articles,
        'author': author
    })

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
    
    return render(request, 'main/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы вошли!')
        else:
            messages.error(request, 'Неверные данные')
    
    return render(request, 'main/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', id=id)
    else:
        form = CommentForm()
    
    return render(request, 'main/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

def articles_list(request, category=None):
    if category:
        articles = Article.objects.filter(category=category)
    else:
        articles = Article.objects.all()
    
    return render(request, 'main/articles_list.html', {
        'articles': articles,
        'current_category': category
    })

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('/articles/')
    else:
        form = ArticleForm()
    
    return render(request, 'main/create_article.html', {'form': form})

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id, user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles_list')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'main/edit_article.html', {'form': form})

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id, user=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('articles_list')
    return render(request, 'main/confirm_delete.html', {'article': article})

def news_list(request):
    news = News.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'main/news_list.html', {'news_list': news})

def news_open(request, news_id):
    news_item = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'main/news_open.html', {'news': news_item})

def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            messages.success(request, 'Новость успешно создана!')
            return redirect('news_open', news_id=news.id)
    else:
        form = NewsForm()
    
    return render(request, 'main/news_create.html', {'form': form})

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            messages.success(request, 'Ваше сообщение отправлено.')
            
            return redirect('feedback')
    else:
        form = FeedbackForm()

    return render(request, 'main/feedback.html', {'form': form})

def index(request):
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        'latest_news': latest_news
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')