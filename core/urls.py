from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # 页面
    path('', views.index, name='index'),
    path('vote/', views.vote_page, name='vote_page'),
    path('suggestion/', views.suggestion_page, name='suggestion_page'),
    
    # API
    path('api/rankings/', views.get_rankings, name='get_rankings'),
    path('api/wordcloud/', views.get_wordcloud, name='get_wordcloud'),
    path('api/vote/', views.submit_vote, name='submit_vote'),
    path('api/suggestion/', views.submit_suggestion, name='submit_suggestion'),
]
