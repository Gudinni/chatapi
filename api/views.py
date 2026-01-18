from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import QuerySet

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer

class ChatListCreateView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatDetailView(APIView):
    def get(self, request, pk: int):
        chat = get_object_or_404(Chat, pk=pk)
        
        raw_limit = request.query_params.get('limit', 20)
        try:
            limit = int(raw_limit)
            if limit < 0: limit = 20
            if limit > 100: limit = 100
        except ValueError:
            limit = 20

        messages_qs = chat.messages.order_by('-created_at')[:limit]
        messages_data = MessageSerializer(messages_qs, many=True).data
        messages_data.sort(key=lambda x: x['created_at'])

        serializer = ChatDetailSerializer(chat, context={'messages_data': messages_data})
        return Response(serializer.data)

    def delete(self, request, pk: int):
        chat = get_object_or_404(Chat, pk=pk)
        chat.delete() # Каскадное удаление сработает на уровне БД/Django
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageCreateView(APIView):
    def post(self, request, pk: int):
        # Проверяем существование чата (Требование 404)
        chat = get_object_or_404(Chat, pk=pk)
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем сообщение, привязывая к чату
            serializer.save(chat=chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
