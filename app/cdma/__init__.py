from flask import Blueprint
cdmaBlueprint = Blueprint('cdmaBlueprint', __name__)
from . import views, errors