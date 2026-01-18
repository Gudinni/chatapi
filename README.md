# Chat API

Тестовое задание: REST API сервис для управления чатами и сообщениями.
Реализовано на Python (Django + DRF) с использованием PostgreSQL и Docker.

## Стек технологий

* **Python** 3.10
* **Django** 5.x
* **Django REST Framework**
* **PostgreSQL** 15
* **Docker** & **Docker Compose**
* **Pytest** 

## Запуск проекта

### Вариант 1: Через Docker

Убедитесь, что у вас установлен Docker и Docker Compose.

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ваш_ник/REPO_NAME.git](https://github.com/Gudinni/chatapi.git)
   cd REPO_NAME

2. **Запустите сборку и контейнеры:**
   ```bash
   docker-compose up --build

3. **Приложение доступно по адресу:** http://localhost:8000/api/chats/


### Вариант 2: Локальный запуск (без Docker)
Если вы хотите запустить проект в виртуальном окружении:

1. **Создайте venv и установите зависимости:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

2. **Примените миграции:**
   ```bash
   python manage.py migrate

3. **Запустите сервер:**
   ```bash
   python manage.py runserver


### API Endpoints
**1. Создать чат**
* **URL: /api/chats/**

* **Method: POST**

* **Body:**
   ```JSON
  
  {
     "title": "Обсуждение проекта"
  }



**2. Отправить сообщение**
* **URL: /api/chats/<id>/messages/**

* **Method: POST**

* **Body:**
   ```JSON

  {
    "text": "Привет! Это первое сообщение."
  }

**3. Получить чат и сообщения**
* **URL: /api/chats/<id>/?limit=20**

* **Method: GET**

* **Query Params: limit (int, default=20, max=100)**

* **Response:**

   ```JSON

      {
        "id": 1,
        "title": "Обсуждение проекта",
        "messages": [
           {"text": "Привет...", "created_at": "..."}
        ]
      }

**4. Удалить чат**
* **URL: /api/chats/<id>/**

* **Method: DELETE**

* **Description: Удаляет чат и каскадно удаляет все связанные сообщения.**

### Тестирование
* **Для запуска тестов используйте:**

   ```Bash
   pytest
   
  ```Или внутри докера:
  docker-compose exec web pytest
