# Trading network
Django web application, with API interface.</br>
_Done as a job placement test task._

### Used technologies: 
 - Required:
   - Python 3.9
   - Django 4.1
   - DRF 3.14
   - Celery 5.2
   - PostgreSQL 15-alpine
   - _(all requirements are met)_
 - My choice:
   - RabbitMQ _(as a message broker for Celery)_
   - AWS SES
   - LocalStack (free local AWS)
   - Docker & docker-compose
   - Swagger _(for testing and reviewing all the endpoints)_
   - Isort _(for sorting imports)_
   - JWT

To start my application on your device you should:
1) have docker-compose installed
2) clone my repo
3) go to the root folder of the project
4) type in terminal `docker-compose up -d`
5) open your browser on `http://localhost:8000/admin/`
6) use admin credentials: **username: "root", password: "112233"**
7) also you can check swagger documentation for API on `http://localhost:8000/swagger/`

Commands to use in application:</br>
`python manage.py raise_debt` - to run celery task for raising unit's debt</br>
`python manage.py reduce_debt` - to run celery task for reducing unit's debt</br>
`python manage.py test_db` -  to fill database with test_data