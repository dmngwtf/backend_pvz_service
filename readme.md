# PVZ Backend Service
<p align="center">
  <h2 align="center">Backend-сервис для управления ПВЗ, приёмками и товарами</h2>
  <p align="center">
    <b>REST API • gRPC • Prometheus-метрики</b><br>
    <b>JWT-авторизация • PostgreSQL • Docker</b>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue" />
    <img src="https://img.shields.io/badge/FastAPI-0.104-green" />
    <img src="https://img.shields.io/badge/gRPC-1.59-blue" />
    <img src="https://img.shields.io/badge/PostgreSQL-15-blue" />
    <img src="https://img.shields.io/badge/Docker-%F0%9F%90%B3-blue" />
    <img src="https://img.shields.io/badge/Prometheus-%F0%9F%93%8A-orange" />
    <img src="https://img.shields.io/badge/JWT-%F0%9F%94%92-brightgreen" />
  </p>
</p>

---

## Возможности
| Функция | Описание |
| --------------------------------- | ----------------------------------------- |
| **REST API** | Управление ПВЗ, приёмками, товарами (порт 8081) с JWT-авторизацией |
| **gRPC-интерфейс** | Получение списка ПВЗ без авторизации (порт 3000) |
| **Prometheus-метрики** | Технические (запросы, задержки) и бизнес-метрики (ПВЗ, приёмки, товары) на порту 9000 |
| **База данных** | PostgreSQL для хранения всех сущностей |
| **Развёртывание** | Docker + docker-compose, отдельные контейнеры для API, gRPC и метрик |
| **Миграции и генерация** | Автоматические миграции БД и генерация gRPC-кода |

---

## Стек
```yaml
Language: Python 3.11
Framework: FastAPI (REST), gRPC
Database: PostgreSQL + SQLAlchemy/AsyncPG
Metrics: Prometheus Client
Auth: JWT (PyJWT)
Deploy: Docker + docker-compose
```
---

## Быстрый старт
```bash
git clone <repository_url>
cd pvz-service
cp .env.example .env  # если есть .env.example, иначе создайте .env вручную
```
---

## Настройка ENV
```env
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/pvz_service
JWT_SECRET=your_jwt_secret_key_123456
```
---

## Запуск через Docker
1. **Миграция БД** (один раз, вне Docker или через exec):
   ```bash
   python src/app/db/migrate.py
   ```
2. **Генерация gRPC-файлов** (один раз):
   ```bash
   python -m grpc_tools.protoc -Iproto --python_out=src/app/grpc --grpc_python_out=src/app/grpc proto/pvz.proto
   ```
3. **Запуск сервисов**:
   ```bash
   docker-compose up -d
   ```
Сервисы подняты: REST API (8081), gRPC (3000), метрики (9000).

Логи:
```bash
docker-compose logs -f app    # REST API
docker-compose logs -f grpc   # gRPC
docker-compose logs -f metrics # Prometheus
```

Коротко по каждому файлу/папке — можно вставить в README как “Project Structure”.

---

### **📁 src/app/api/routes/**
Маршруты REST API.
* **auth.py** — аутентификация и JWT-токены.
* **pvz.py** — CRUD-операции с ПВЗ.
* **receptions.py** — управление приёмками.
* **products.py** — работа с товарами.

---

### **📁 src/app/core/**
Ядро приложения.
* **config.py** — загрузка настроек и ENV.
* **logging.py** — конфигурация логирования.
* **metrics.py** — определение Prometheus-метрик.

---

### **📁 src/app/db/**
Работа с PostgreSQL.
* **database.py** — подключение, сессии, инициализация.
* **migrate.py** — скрипт миграций (Alembic или кастомный).

---

### **📁 src/app/grpc/**
gRPC-сервер и сгенерированный код.
* **server.py** — запуск gRPC-сервера.
* **pvz_pb2.py** / **pvz_pb2_grpc.py** — сгенерированные файлы из .proto.

---

### **📁 src/**
* **main.py** — точка входа FastAPI (REST).
* **main_metrics.py** — Prometheus HTTP-сервер.

---

### **📁 tests/**
* **test_api.py** — тесты REST API (pytest).
* **test_grpc.py** — тесты gRPC.

---

### **📁 proto/**
* **pvz.proto** — Protobuf-описание gRPC-сервиса.

---

### **Корневые файлы**
* **docker-compose.yml** — оркестрация контейнеров.
* **Dockerfile** — образ для REST API.
* **Dockerfile.metrics** — образ для Prometheus-метрик.
* **Dockerfile.grpc** — образ для gRPC-сервера.
* **requirements.txt** — зависимости Python.
* **logs/app.log** — файл логов (монтируется в контейнер).

---