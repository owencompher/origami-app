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
    if request.args.get('tag'):
        tags = [request.args.get('tag')]
        models = [tag.moodel for tag in MoodelTags.select().join(Tag).where(Tag.name==tags[0])]
    else:
        tags = [] 
        models = Moodel.select()

    for model in models: model.gatherTags()

    return render_template('model/index.html', models=models, tags=tags)


@bp.route('/model/<int:model_id>')
def model(model_id):
    model = get_object_or_404(Moodel.select().where(Moodel.id==model_id))
    model.tags = Tag.select().join(MoodelTags).join(Moodel).where(Moodel.id==model.id)
    return render_template('model/model.html', model=model)
