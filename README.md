# api_yamdb

### Описание

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

### Алгоритм регистрации пользователей

1.Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.    
2.YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.    
3.Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).   
4.При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).    

### Пользовательские роли

**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.    
**Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.    
**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.    
**Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.    
**Суперюзер Django** — обладет правами администратора (admin)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/CeaPanochka/api_yatube
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```
Заполнить базу данных. Последовательно выполнить семь команд:

```
python3 manage.py import_users
```

```
python3 manage.py import_categories
```

```
python3 manage.py import_genres
```

```
python3 manage.py import_titles
```

```
python3 manage.py import_genre_titles
```

```
python3 manage.py import_reviews
```

```
python3 manage.py import_comments
```

Запустить проект:

```
python3 manage.py runserver
```


### Примеры запросов:

#### AUTH
Регистрация нового пользователя: 

```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```

Получение JWT-токена: 

```
POST http://127.0.0.1:8000/api/v1/auth/token/
```

#### CATEGORIES
Получение списка всех категорий: 
```
GET http://127.0.0.1:8000/api/v1/categories/
```

Добавление новой категории:

```
POST http://127.0.0.1:8000/api/v1/categories/
```

Удаление категории:

```
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```

#### GENRES

Получение списка всех жанров:

```
GET http://127.0.0.1:8000/api/v1/genres/
```

Добавление жанра: 

```
POST http://127.0.0.1:8000/api/v1/genres/
```

Удаление жанра:

```
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```

#### TITLES

Получение списка всех произведений:

```
GET http://127.0.0.1:8000/api/v1/titles/
```

Добавление произведения:

```
POST http://127.0.0.1:8000/api/v1/titles/
```

Получение информации о произведении:

```
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Частичное обновление информации о произведении:

```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Удаление произведения:

```
DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

#### REVIEWS

Получение списка всех отзывов:

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Добавление нового отзыва:

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Полуение отзыва по id:

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Частичное обновление отзыва по id:

```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Удаление отзыва по id:

```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

#### COMMENTS

Получение списка всех комментариев к отзыву:

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Добавление комментария к отзыву:

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Получение комментария к отзыву:

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Частичное обновление комментария к отзыву:

```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Удаление комментария к отзыву

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

#### USERS

Получение списка всех пользователей:

```
GET http://127.0.0.1:8000/api/v1/users/
```

Добавление пользователя:

```
POST http://127.0.0.1:8000/api/v1/users/
```

Получение пользователя по username:

```
GET http://127.0.0.1:8000/api/v1/users/{username}/
```

Изменение данных пользователя по username:

```
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
```

Удаление пользователя по username:

```
http://127.0.0.1:8000/api/v1/users/{username}/
```

Получение данных своей учетной записи:

```
GET http://127.0.0.1:8000/api/v1/users/me/
```

Изменение данных своей учетной записи:

```
PATCH http://127.0.0.1:8000/api/v1/users/me/
```