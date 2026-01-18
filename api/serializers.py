from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at']

    def validate_title(self, value: str) -> str:
        """Тримминг пробелов и проверка на пустоту."""
        title = value.strip()
        if not title:
            raise serializers.ValidationError("Title cannot be empty.")
        return title

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat_id', 'text', 'created_at']
        read_only_fields = ['chat_id', 'created_at']

    def validate_text(self, value: str) -> str:
        text = value.strip()
        if not text:
            raise serializers.ValidationError("Text cannot be empty.")
        return text

class ChatDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для GET /chats/{id} с вложенными сообщениями."""
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'messages']

    def get_messages(self, obj) -> list:
        return self.context.get('messages_data', [])