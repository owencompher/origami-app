from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_peewee.utils import get_object_or_404
from app import db
from orm import *

bp = Blueprint('model', __name__)

@bp.route('/')
def index():
    tags = []
    name = None
    if request.args.get('tag'): tags = request.args.get('tag').split(' ')
    if request.args.get('tags'): tags = request.args.get('tags').split(' ')

    if request.args.get('name'):
        name = request.args.get('name')

    filterText = []
    
    if tags: 
        models = (Moodel.select()
                        .join(MoodelTags)
                        .join(Tag)
                        .where(Tag.name<<tags)
                        .group_by(Moodel)
                        .having(fn.COUNT(Tag.name) == len(tags)))
        filterText.append(f"with tag{'s' if len(tags)>1 else ''}: " + ', '.join(tags))

    else: models = Moodel.select()

    if name: 
        models = models.select().where(Moodel.name**f'%{name}%')
        filterText.append(f"with name containing \"{name}\"")

    models = [model.gatherTags() for model in models]

    return render_template('model/index.html', models=models, filterText=filterText)


@bp.route('/model/<int:model_id>')
def model(model_id):
    model = get_object_or_404(Moodel.select().where(Moodel.id==model_id))
    model.tags = Tag.select().join(MoodelTags).join(Moodel).where(Moodel.id==model.id)
    return render_template('model/model.html', model=model)
