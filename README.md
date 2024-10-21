
# Проект управления отходами API

Этот проект реализует RESTful API для управления организациями, хранилищами и передачей отходов. С использованием Django и Django REST Framework (DRF), система предоставляет возможности управления для организаций и хранилищ с поддержкой автоматической документации Swagger.

## Инструкция по деплою

### Предварительные требования

- Установлен Docker
- Установлен Docker Compose

### Шаги установки

1. Клонируйте репозиторий
2. Перейдите в каталог проекта
3. Соберите и запустите контейнеры: docker-compose up --build  
4. Примените миграции: docker-compose run web python manage.py migrate
5. (При необходимости) Остановите контейнеры: docker-compose down
   

## Генерация тестовых данных

Для генерации тестовых данных используйте скрипт populate_data.py.

1. Подключитесь к контейнеру
2. Запустите скрипт: python populate_data.py
   
## Тестирование

unit-тесты основных методов API реализованы в файле test.py. Для запуска тестов выполните:
python manage.py test

## Документация API
### Доступные API Эндпоинты

- Организации:
  - GET /organizations/ - Получение списка организаций
  - POST /organizations/ - Создание новой организации
  - GET /organizations/<id>/ - Получение, обновление или удаление определенной организации

- Хранилища:
  - GET /storages/ - Получение списка хранилищ
  - POST /storages/ - Создание нового хранилища
  - GET /storages/<id>/ - Получение, обновление или удаление определенного хранилища

- Передача отходов:
  - POST /waste_transfer/ - Передача отходов в подходящее хранилище


Автоматически сгенерированная документация API доступна по адресу: http://localhost:8000/swagger/
