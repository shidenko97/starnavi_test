# Starnavi test exercise
Just a Starnavi test exercise 

## Explanation
[Test task file](task.pdf)

## Setup
All you need to setup the application is to install requirements from
[requirements.txt](requirements.txt) file and run following commands:
```
python manage.py migrate
python manage.py runserver
```

## API endpoints for task
User signup (Returns user instance)
```
POST http://127.0.0.1:8000/api/users/
Params: {"username":"{username}", "password":"{password}"}
```
User login (Returns JWT token)
```
POST http://127.0.0.1:8000/api/auth
Params: {"username":"{username}", "password":"{password}"}
```
Post creation (Returns post instance)
```
POST http://127.0.0.1:8000/api/posts/
Params: {"title":"{title}", "body":"{body}"}
Headers: {"Authorization":"JWT {token}"}
```
Post like/unlike (Returns information message)
```
GET http://127.0.0.1:8000/api/posts/like/{post_id}/
Headers: {"Authorization":"JWT {token}"}
```
Post dislike/undislike (Returns information message)
```
GET http://127.0.0.1:8000/api/posts/dislike/{post_id}/
Headers: {"Authorization":"JWT {token}"}
```
Likes/dislikes analytics grouped by day (Returns a list of objects)
```
GET http://127.0.0.1:8000/api/posts/analytics/?date_from={date_from}&date_to={date_to}
Headers: {"Authorization":"JWT {token}"}
```
User's last login and last API request (Returns an object with 2 params)
```
GET http://127.0.0.1:8000/api/users/activity/{post_id}/
Headers: {"Authorization":"JWT {token}"}
```
