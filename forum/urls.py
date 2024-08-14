from django.urls import path
from forum.views import ThreadListView, ThreadDetailView, ThreadCreateView

app_name = 'forum'

urlpatterns = [
    path('', ThreadListView.as_view(), name='thread_list'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('create/', ThreadCreateView.as_view(), name='thread_create'),
]