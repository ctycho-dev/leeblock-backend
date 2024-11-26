# FastApi application for leeblock.ru

* run redis for test
redis-server


* Run for production
gunicorn --bind=0.0.0.0:5000 --workers=4 --worker-class uvicorn.workers.UvicornWorker --threads=4 main:app