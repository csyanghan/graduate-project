import os
import multiprocessing
debug = False
bind = "0.0.0.0:5000"
pidfile = "gunicorn.pid"
accesslog="./flask_app.log"
workers = multiprocessing.cpu_count()*2 + 1
daemon=True
