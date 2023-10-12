# DjangoChatLast

# Проект
Это приложение чат-комнат, разработанное с использованием Django.

# Установка и запуск
1. Клонируйте репозиторий на локальную машину:

git clone https://github.com/pltnv123/DjangoChatLast.git
2. Установите зависимости проекта:

pip install -r requirements.txt
3. Примените миграции базы данных:

python manage.py migrate
4. Создайте суперпользователя (по желанию):

python manage.py createsuperuser
5. Запустите сервер разработки:

python manage.py runserver
Приложение будет доступно по адресу http://localhost:8000/.

# Использование
1. Перейдите по адресу http://localhost:8000/rooms/ в браузере, чтобы просмотреть список доступных чат-комнат.
2. Чтобы войти в чат-комнату, нажмите на неё. В чат-комнате вы можете просматривать историю сообщений и список онлайн-пользователей.
3. Вы также можете создавать новые чат-комнаты и загружать аватары для своего профиля.

# API-интерфейс
Приложение также предоставляет следующие API-эндпоинты:

* GET /api/rooms/: Получить список всех чат-комнат.
* POST /api/rooms/: Создать новую чат-комнату.
* GET /api/rooms/{id}/: Получить подробную информацию о конкретной чат-комнате.
* GET /api/messages/: Получить список всех сообщений.
* POST /api/messages/: Отправить новое сообщение.
* GET /api/profiles/: Получить список всех профилей пользователей.
* POST /api/profiles/: Создать профиль нового пользователя.

Дополнительную информацию об API можно найти в документации API.

# Технологии
* Django 4.2.4
* Django REST Framework 3.14.0
* Channels 4.0.0
