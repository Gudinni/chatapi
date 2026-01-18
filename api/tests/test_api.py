import pytest
from rest_framework.test import APIClient
from api.models import Chat, Message

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def chat():
    return Chat.objects.create(title="Test Chat")

@pytest.mark.django_db
def test_create_chat(client):
    """Тест создания чата"""
    response = client.post('/api/chats/', {'title': '  New Chat  '})
    assert response.status_code == 201
    assert response.data['title'] == 'New Chat' # Проверка тримминга
    assert Chat.objects.count() == 1

@pytest.mark.django_db
def test_create_message(client, chat):
    """Тест создания сообщения в существующий чат"""
    url = f'/api/chats/{chat.id}/messages/'
    response = client.post(url, {'text': 'Privet'})
    assert response.status_code == 201
    assert response.data['text'] == 'Privet'
    assert Message.objects.count() == 1

@pytest.mark.django_db
def test_create_message_invalid_chat(client):
    """Тест отправки в несуществующий чат (404)"""
    response = client.post('/api/chats/999/messages/', {'text': 'Fail'})
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_chat_with_limit(client, chat):
    """Тест лимита сообщений"""
    # Создаем 25 сообщений
    for i in range(25):
        Message.objects.create(chat=chat, text=f"msg {i}")

    # Запрашиваем дефолт (20)
    response = client.get(f'/api/chats/{chat.id}/')
    assert len(response.data['messages']) == 20
    # Проверяем, что вернулись последние (msg 24 должен быть последним)
    assert response.data['messages'][-1]['text'] == "msg 24"

    # Запрашиваем limit=10
    response = client.get(f'/api/chats/{chat.id}/?limit=10')
    assert len(response.data['messages']) == 10

@pytest.mark.django_db
def test_delete_chat_cascade(client, chat):
    """Тест каскадного удаления"""
    Message.objects.create(chat=chat, text="To be deleted")
    
    response = client.delete(f'/api/chats/{chat.id}/')
    assert response.status_code == 204
    
    assert Chat.objects.count() == 0
    assert Message.objects.count() == 0 