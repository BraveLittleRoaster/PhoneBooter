from celery import Celery
app = Celery('hello', broker='amqp://guest@localhost//')

@app.task
def add(x, y): return x + y

if __name__ == '__main__':
    app.worker_main()