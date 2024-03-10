# auth-and-promotion
## Set up
1. Build up a postgres DB: Following deployment/postgres.sh
2. Build up a redis: Following deployment/redis.sh
3. Build up a kafka: Following deployment/kafka.sh
4. Install dependencies:
```
pip install -r requirements.txt
```

## Start services:
At /app directory,
1. Auth service
```
python app/auth/main.py
```
2. User service
```
python app/user/main.py
```
3. Promotion service
```
python app/promotion/main.py
```

## Start workers
At /app directory,
1. Celery beat
```
celery -A app.common.celery_app.tasks beat -l info
```
2. Celery default worker
```
celery -A app.common.celery_app.tasks worker -l info -Q default
```
