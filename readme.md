# PVZ Backend Service

Сервис для управления пунктами выдачи заказов (ПВЗ), приёмками и товарами. Реализует REST API, gRPC и Prometheus-метрики, используя PostgreSQL для хранения данных.

## Описание

Проект предоставляет backend-сервис с тремя основными интерфейсами:
- **REST API** (порт 8081): Управление ПВЗ, приёмками, товарами с JWT-авторизацией.
- **gRPC** (порт 3000): Получение списка ПВЗ без авторизации.
- **Prometheus-метрики** (порт 9000): Технические (запросы, задержки) и бизнес-метрики (ПВЗ, приёмки, товары).

Используется Docker для развертывания, PostgreSQL для данных, Python 3.11 с FastAPI, gRPC и Prometheus.

## Требования

- Docker и Docker Compose
- Python 3.11+ (для разработки и тестов)
- `make` (опционально, для удобства)

## Установка

1. **Клонируйте репозиторий**:
   git clone <repository_url>
   cd pvz-service

2. **Создайте .env**:
    DATABASE_URL=postgresql://postgres:yourpassword@db:5432/pvz_service
    JWT_SECRET=your_jwt_secret_key_123456
3. **Сгенерируйте gRPC-файлы**:
    python -m grpc_tools.protoc -Iproto --python_out=src/app/grpc --grpc_python_out=src/app/grpc proto/pvz.proto
4. **Запустите сервисы**:
    docker-compose up -d

**Структура прокта**:
```
pvz-service/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py       # аутентификация
│   │   │   │   ├── pvz.py        # ПВЗ
│   │   │   │   ├── receptions.py # приёмки
│   │   │   │   ├── products.py   # товары
│   │   ├── core/
│   │   │   ├── config.py         # настройки
│   │   │   ├── logging.py        # логирование
│   │   │   ├── metrics.py        # метрики
│   │   ├── db/
│   │   │   ├── database.py       # подключение к БД
│   │   ├── grpc/
│   │   │   ├── server.py         # gRPC-сервер
│   │   │   ├── pvz_pb2.py        # сгенерированный код
│   │   │   ├── pvz_pb2_grpc.py   # сгенерированный код
│   │   ├── main.py               # FastAPI приложение
│   │   ├── main_metrics.py       # Prometheus-сервер
│   ├── tests/
│   │   ├── test_api.py           # тесты REST API
│   │   ├── test_grpc.py          # тесты gRPC
├── proto/
│   ├── pvz.proto                 # gRPC-протобуфер
├── logs/
│   ├── app.log                   # логи
├── .env                          # переменные окружения
├── docker-compose.yml            # Docker-конфигурация
├── Dockerfile                    # для REST API
├── Dockerfile.metrics            # для метрик
├── Dockerfile.grpc               # для gRPC
├── requirements.txt              # зависимости
├── README.md                     # докуметация
```


