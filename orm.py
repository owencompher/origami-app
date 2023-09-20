from peewee import *
from flask_login import UserMixin
from flask_admin.contrib.peewee import ModelView

from app import db


class User(db.Model, UserMixin):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    joined = DateTimeField()
    admin = BooleanField(default=False)

    def __str__(self): return self.username


class Moodel(db.Model):
    name = CharField()
    designer = CharField()
    user = ForeignKeyField(User, backref='moodels')
    posted = DateTimeField()
    description = TextField()

    def gatherTags(self):
        self.tags = [tag.tag for tag in self.tags] #Tag.select().join(MoodelTags).join(Moodel).where(Moodel.id==self.id)

    def __str__(self): return self.name


class Tag(db.Model):
    name = CharField()

    def __str__(self): return self.name


class MoodelTags(db.Model):
    moodel = ForeignKeyField(Moodel, backref='tags')
    tag = ForeignKeyField(Tag, backref='moodels')
    class Meta:
        indexes = ((('moodel', 'tag'), True),)
