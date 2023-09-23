from datetime import datetime
from markdown import markdown
from markupsafe import escape
from app import app, db
from orm import *

import admin

import auth
app.register_blueprint(auth.bp)

import model
app.register_blueprint(model.bp)
app.add_url_rule('/', endpoint='index')

@app.template_filter()
def dtFormat(datetime):
    delta = datetime.now() - datetime
    if delta.days > 550: string = str(round(delta.days/365)) + " years ago"
    elif delta.days > 185: string = " a year ago"
    elif delta.total_seconds() > 130000: string = str(round(delta.total_seconds()/86400)) + " days ago"
    elif delta.total_seconds() > 86000: string = " a day ago"
    elif delta.total_seconds() > 5400: string = str(round(delta.total_seconds()/3600)) + " hours ago"
    elif delta.total_seconds() > 3500: string = " an hour ago"
    elif delta.total_seconds() > 90: string = str(round(delta.total_seconds()/60)) + " minutes ago"
    elif delta.total_seconds() > 50: string = " a minute ago"
    else: string = str(round(delta.total_seconds())) + " seconds ago"
    return string

@app.template_filter()
def md(text): return markdown(escape(text))

def create_tables():
    db.database.create_tables([User, Moodel, Tag, MoodelTags], safe=True)

if __name__ == '__main__':
    create_tables()
    app.run()
