!!! IT MUST BE RUN ONLY FOR THE PROD. DB IN SERVER PC !!!

Generate a version with a message (not too long at all!)
```
alembic revision --autogenerate -m "Your message"
```

Do the migration - upgrade head
```
alembic upgrade head
```