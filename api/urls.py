from django.urls import path
from .views import ChatListCreateView, ChatDetailView, MessageCreateView

urlpatterns = [
    path('chats/', ChatListCreateView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chats/<int:pk>/messages/', MessageCreateView.as_view(), name='message-create'),
]