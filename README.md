#Реализация интернет-магазина с авторизацией, аутентификацией и хешированием паролей с помощью bcrypt 
две роли:
Продавец: создаёт, изменяет и удаляет свои товары.
Покупатель: может просматривать товары и категории.
использую jwt-token
в app/models/users.py модель юзер
в app/schemas.py модели UserCreate, User, с помощью pydantic валидируем данные
в app/routers/users.py роутеры регистрации

#быстрый старт:
  py -m venv venv

  pip install -r requirements.txt

  uvicorn app.main:app --reload

  http://127.0.0.1:8000/docs
