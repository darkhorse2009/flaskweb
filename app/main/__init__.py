from flask import Blueprint
mainBlueprint = Blueprint('mainBlueprint', __name__)
from . import views, errors