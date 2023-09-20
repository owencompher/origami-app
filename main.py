from app import app, db
from orm import *

import admin

import auth
app.register_blueprint(auth.bp)

import model
app.register_blueprint(model.bp)
app.add_url_rule('/', endpoint='index')


def create_tables():
    db.database.create_tables([User, Moodel, Tag, MoodelTags], safe=True)

if __name__ == '__main__':
    create_tables()
    app.run()
