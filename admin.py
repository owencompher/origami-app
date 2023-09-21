from app import app
from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from orm import *

class AuthView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.path))

class MoodelView(AuthView, ModelView):
    column_hide_backrefs = False
    inline_models = [MoodelTags]
    column_list = ('id', 'name', 'designer', 'user', 'description')

class IndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.path))


admin = Admin(app, name="admin", index_view=IndexView())
admin.add_view(AuthView(User))
admin.add_view(MoodelView(Moodel))
admin.add_view(AuthView(Tag))
admin.add_view(AuthView(MoodelTags))
