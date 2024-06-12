Generic single-database configuration.

Generate a version with a message (not too long at all!)
```
alembic revision --autogenerate -m "Your message"
```

Do the migration - upgrade head
```
alembic upgrade head
```