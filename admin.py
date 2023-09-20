from app import app
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from orm import *

class AuthView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class MoodelView(AuthView):
    column_hide_backrefs = False
    inline_models = [MoodelTags]
    column_list = ('id', 'name', 'designer', 'user', 'description')


admin = Admin(app, name="admin")
admin.add_view(AuthView(User))
admin.add_view(MoodelView(Moodel))
admin.add_view(AuthView(Tag))
admin.add_view(AuthView(MoodelTags))
