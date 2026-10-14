# FastAPI Library Management System

یک سیستم مدیریت کتابخانه ساده که با فریم‌ورک FastAPI و ذخیره‌سازی موقت در حافظه پیاده‌سازی شده است.

## Endpoints
- `GET /books` - دریافت لیست تمام کتاب‌ها
- `POST /books` - ثبت کتاب جدید
- `GET /books/{id}` - دریافت مشخصات یک کتاب با شناسه
- `PATCH /books/{id}` - ویرایش اطلاعات کتاب
- `DELETE /books/{id}` - حذف کتاب

## Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload