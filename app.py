from flask import Flask
from flask_peewee.db import Database
from werkzeug.middleware.proxy_fix import ProxyFix

SECRET_KEY = # 
DATABASE = {
    'name': 'database',
    'engine': 'peewee.SqliteDatabase',
}

app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

db = Database(app)
