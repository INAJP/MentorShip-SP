# FastAPI Library Management System

یک سیستم مدیریت کتابخانه ساده که با فریم‌ورک **FastAPI** ساخته شده است. داده‌ها داخل حافظه (متغیرهای پایتون) نگهداری می‌شوند و دیتابیسی لازم نیست.

## امکانات

- مشاهده لیست همه کتاب‌ها
- ثبت کتاب جدید
- مشاهده اطلاعات یک کتاب مشخص
- ویرایش بخشی از اطلاعات یک کتاب (PATCH)
- حذف کتاب
- اعتبارسنجی ورودی‌ها با Pydantic
- مستندات تعاملی خودکار (Swagger UI)

## تکنولوژی‌ها

- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic v2

## نصب و اجرا

```bash
# 1. کلون کردن پروژه
git clone <repo-url>
cd <repo-folder>

# 2. (اختیاری) ساخت و فعال‌سازی محیط مجازی
python -m venv venv
venv\Scripts\activate        # ویندوز
# source venv/bin/activate   # لینوکس و مک

# 3. نصب پکیج‌ها
pip install -r requirements.txt

# 4. اجرای سرور
uvicorn main:app --reload
```

سرور روی `http://127.0.0.1:8000` اجرا می‌شود.

مستندات تعاملی که می‌توانید همه endpointها را در آن تست کنید:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| متد | مسیر | توضیح | کد موفقیت |
|--------|---------------|-------------------------------|-----------|
| GET | `/books` | دریافت لیست همه کتاب‌ها | 200 |
| POST | `/books` | ثبت کتاب جدید | 201 |
| GET | `/books/{id}` | دریافت اطلاعات یک کتاب | 200 |
| PATCH | `/books/{id}` | ویرایش اطلاعات یک کتاب | 200 |
| DELETE | `/books/{id}` | حذف یک کتاب | 200 |

## مدل داده

| فیلد | نوع | الزامی | قوانین |
|---------|--------|--------|-------------------------|
| id | int | - | به صورت خودکار ساخته می‌شود |
| title | string | بله | حداقل ۱ کاراکتر |
| author | string | بله | حداقل ۱ کاراکتر |
| year | int | بله | بزرگ‌تر از ۰ |
| summary | string | خیر | می‌تواند `null` باشد |

## نمونه درخواست‌ها

### ثبت کتاب جدید

```bash
curl -X POST http://127.0.0.1:8000/books -H "Content-Type: application/json" -d "{\"title\": \"Clean Code\", \"author\": \"Robert C. Martin\", \"year\": 2008, \"summary\": \"A handbook of agile software craftsmanship\"}"
```

پاسخ:

```json
{
  "message": "Book created successfully",
  "book": {
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "year": 2008,
    "summary": "A handbook of agile software craftsmanship",
    "id": 1
  }
}
```

### دریافت لیست کتاب‌ها

```bash
curl http://127.0.0.1:8000/books
```

### دریافت یک کتاب

```bash
curl http://127.0.0.1:8000/books/1
```

### ویرایش کتاب

فقط فیلدهایی که می‌فرستید تغییر می‌کنند:

```bash
curl -X PATCH http://127.0.0.1:8000/books/1 -H "Content-Type: application/json" -d "{\"year\": 2009}"
```

### حذف کتاب

```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

## خطاها

| کد | معنی |
|-----|------|
| 404 | کتابی با این شناسه پیدا نشد |
| 422 | داده‌های ورودی نامعتبر است (مثلاً `title` خالی یا `year` منفی) |

نمونه پاسخ خطای ۴۰۴:

```json
{ "detail": "Book not found" }
```

## ساختار پروژه

```
.
├── main.py            # کد اصلی برنامه
├── requirements.txt   # وابستگی‌ها
├── .gitignore
└── README.md
```

## نکات

- داده‌ها فقط در حافظه نگهداری می‌شوند و **با هر بار ری‌استارت سرور پاک می‌شوند**.
- شناسه‌ی کتاب‌ها از ۱ شروع می‌شود و با هر کتاب جدید یکی زیاد می‌شود. شناسه‌ی کتاب حذف‌شده دوباره استفاده نمی‌شود.
- در ویندوز اگر از PowerShell استفاده می‌کنید، به جای `curl` از `curl.exe` استفاده کنید یا مستقیماً از `/docs` تست کنید.