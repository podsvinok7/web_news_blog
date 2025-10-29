from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm, NewsForm
from .models import Feedback
from .models import News
from django.shortcuts import get_object_or_404 

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