from django.urls import path
from apps.news import views
from apps.news.feeds import NewsRSSFeed, NewsAtomFeed

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('rss/', NewsRSSFeed(), name='news_rss'),
    path('atom/', NewsAtomFeed(), name='news_atom'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
]
