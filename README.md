
# Agile-system

**Agile-system** — bu **Jira/Trello** kabi Agile metodologiyasiga asoslangan vazifa (task) boshqaruv tizimi. Loyihada foydalanuvchilar rollar orqali bir-biriga bog‘langan, har bir rol o‘ziga xos ruxsatlarga ega. Loyihaning asosiy maqsadi — task lifecycle'ni real vaqtda boshqarish va kuzatish.

---

## Texnologiyalar

- Python 3.12  
- Django 5.x  
- Django REST Framework  
- JWT Authentication (SimpleJWT)  
- WebSocket (`channels`, `channels_redis`)  
- Celery + Redis (background task va email bildirishnomalar uchun) 
- django-query-counter optimizatsiya uchun
- Swagger (drf-yasg)  
- PostgreSQL  
- Flower (Celery monitoring)  
- Faker (test userlar uchun)

---

## Rollar va Imkoniyatlar

| Rol              | Imkoniyatlar |
|------------------|--------------|
| **Project Owner** | Loyihani yaratish, ro'yhatdan o'tkazish, rollarni tayinlash |
| **Project Manager** | Task yaratish, assignee tanlash, status va priority o'zgartirish |
| **Developer**    | `To Do → In Progress → Ready for Testing` holatlarini o‘zgartirish |
| **Tester**       | Taskni **qabul qilish (✅ Done)** yoki **rad etish (❌ To Do)** |

---

## O‘rnatish

```bash
git clone https://github.com/Jamshidbekpy/Agile-system.git
cd Agile-system
python -m venv venv
source venv/bin/activate  # yoki Windows: venv\Scripts\activate
pip install -r requirements/develop.txt
```

### .env misoli

```
SECRET_KEY=django-insecure-123
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgres://user:password@localhost:5432/agile_db

REDIS_URL=redis://localhost:6379

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=yourpassword
EMAIL_USE_TLS=True
```

---

## Ishga tushirish

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Celery orqali email yuborish

```bash
# redis-server terminalda ochiq bo'lishi kerak
redis-server

# Celery
celery -A config worker -l info

```

---

## Auth: JWT

- `api/token/` – Login (email + password)
- `api/token/refresh/` – Token yangilash
- `api/token/verify/` – Token tekshirish

---

## Real Time: WebSocket

- Redis orqali kanal xabarlari yuboriladi (`channels`)
- `High Priority` tasklar barcha userlarga real vaqt rejimida bildirish sifatida yuboriladi

---

## Xabarnomalar

| Holat                    | Kimga yuboriladi |
|--------------------------|------------------|
| Tayinlangan              | Developer / Tester |
| Status: In Progress      | Project Manager    |
| Ready for Testing        | Tester             |
| Rejected                 | Developer          |
| **High Priority task**   | **Barcha**         |

Bildirishnomalar:
- WebSocket orqali (`channel_layer.group_send`) + chat so'zlashuv
- Email orqali (Celery + Django Email)

---

## API Endpoints

| Endpoint | Tavsif | Method | Permission |
|----------|--------|--------|------------|
| `/api/v1/tasks/` | Task ro'yxati -> low,medium,high bo'yicha tartib / yaratish/| GET, POST | Manager |
| `/api/v1/tasks/<id>/` | Task detallari | GET, PUT, DELETE | Har xil rollar |
| `/api/v1/tasks/<id>/change_status/` | Manager or Developer o'zgartiradi | POST | Developer |
| `/api/v1/tasks/<id>/approve/` | Tester qabul qiladi | POST | Tester |
| `/api/v1/tasks/<id>/reject/` | Tester rad etadi | POST | Tester |
|`/api/v1/tasks/<id>/assign/` | Project Ower loyihaga a'zolar qo'shadi | POST | Project Owner (creator) |
|`/api/v1/tasks/<id>/change_priority/` | Project Manager ustuvorlikni o'zgartiradi | POST | Project Manager|
| `/api/v1/tasks/<id>/history/` | Task tarixi | GET | Har kim |
| `/api/v1/users/register/` | Ro‘yxatdan o‘tish | POST | - |
| `/api/v1/users/login/` | Login (JWT) | POST | - |
| `/api/v1/users/assign-role/<int:pk>/` | Rolga tayinlash | POST | Project Owner |


---

## Test foydalanuvchilar yaratish

```bash
python manage.py init_users 10
```

Bu komandani ishga tushirsangiz, 10 ta turli rollarga ega `Faker` asosidagi foydalanuvchilar yaratiladi.

---

## Qo'shimcha

task.admin da task prioritylari UI da ko'rsatiladi low > yashil, medium > sariq, high > qizil

---

## Swagger

API'ni vizual test qilish:
```
http://localhost:8000/swagger/
```

---

## Muallif

**Jamshidbek Shodibekov**  
GitHub: [@Jamshidbekpy](https://github.com/Jamshidbekpy)

---

## Litsenziya

MIT License – `Agile-system` ochiq kodli loyiha.
