from app import app, db
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask_login import LoginManager
from orm import *

admin = Admin(app, name="admin")
admin.add_view(ModelView(User))
admin.add_view(MoodelView(Moodel))
admin.add_view(ModelView(Tag))
admin.add_view(ModelView(MoodelTags))

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
