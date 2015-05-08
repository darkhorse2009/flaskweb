from flask import request, render_template, g, session, redirect, url_for
from .. import mysql
from . import mainBlueprint
from contextlib import closing

@mainBlueprint.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('main/base.html')