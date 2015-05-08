from flask import request, render_template, g, session, redirect, url_for, flash
from .. import mysql
from . import lteBlueprint
from . import SQLHelper
# from .importdb import importxls
from collections import Counter
from contextlib import closing

def connect_db():
    return  mysql.connection

def init_db():
    pass

def runScript(scriptName):
    with closing(connect_db()) as db:
        pass
    db.commit()

@lteBlueprint.before_request
def before_request():
    g.db = connect_db()

#主页
#获得表列表
@lteBlueprint.route('/Profile', methods=['GET', 'POST'])
def Profile():
    allTableNames = SQLHelper.getAllTableNames(connect_db())
    # print(type(allTableNames), ":", allTableNames)
    return render_template('lte/profile.html', allTableNames=allTableNames)

#显示表配置字段
@lteBlueprint.route('/showTableProfile/<tableName>', methods=['GET', 'POST'])
def showTableProfile(tableName):
    allTableNames = SQLHelper.getAllTableNames(connect_db())
    workingFields = SQLHelper.getWorkingField(connect_db(), tableName)
    if workingFields :
        return render_template('lte/showPrifile.html', allTableNames=allTableNames, workingFields=workingFields, tableName=tableName)
    else:
        print('success!')
        return redirect(url_for('lteBlueprint.editProfileTable', tableName=tableName))


#获得表的所有字段
@lteBlueprint.route('/editProfile/<tableName>', methods=['GET', 'POST'])
def editProfileTable(tableName):
    session['s_tableName'] = tableName
    allTableNames = SQLHelper.getAllTableNames(connect_db())
    workingFields = SQLHelper.getWorkingField(connect_db(), tableName)
    tableValues = SQLHelper.getTableFields(connect_db(), tableName)
    return render_template('lte/editProfile.html', allTableNames=allTableNames, tableName=tableName, tableValues=tableValues,workingFields=workingFields)



#更新配置字段
@lteBlueprint.route('/updateProfile/<tableName>', methods=['GET', 'POST'])
def updateProfileValue(tableName):
    if request.method=='POST':
        print(tableName)
        print(request.form.getlist('option1'))
        profileValues=request.form.getlist('option1')
        SQLHelper.updateProfile(connect_db(), tableName, profileValues)
        print('success')
    return redirect(url_for('lteBlueprint.showTableProfile', tableName=tableName))

@lteBlueprint.route('/initdb', methods=['GET', 'POST'])
def initdb():
    SQLHelper.importxls(connect_db(), 'test.xlsx')
    return redirect(url_for('.lte'))

@lteBlueprint.route('/lteCategories', methods=['GET', 'POST'])
def lteCategories():
    page = request.args.get('p', 1)
    limit = request.args.get('limit', 9)
    offset = (int(page)-1) * int(limit)

    categories = []
    allTableNames = SQLHelper.getAllTableNames(connect_db())
    for tableName in allTableNames:
        try:
            maxCount = SQLHelper.getMaxRecord(connect_db(), tableName)
            minCount = SQLHelper.getMinRecord(connect_db(), tableName)
            categories.append([tableName, maxCount[0], minCount])
        except:
            print(tableName)

    total = len(categories)
    pager = {'total':int(total), 'limit':int(limit), 'curr_page':int(page)}
    categories = categories[int(offset):int(offset)+int(limit)-1]
    return render_template('lte/categories.html', categories=categories, p=pager)

@lteBlueprint.route('/lteCategories/detailMax/<tableName>')
def detailMax(tableName):
    page = request.args.get('p', 1)
    limit = request.args.get('limit', 9)
    offset = (int(page)-1) * int(limit)

    maxAllRecord = SQLHelper.getMaxAllRecord(connect_db(), tableName)[1]
    maxAllField = SQLHelper.getMaxAllRecord(connect_db(), tableName)[0]

    total = len(maxAllRecord)
    pager = {'total':int(total), 'limit':int(limit), 'curr_page':int(page)}
    maxAllRecord = maxAllRecord[int(offset):int(offset)+int(limit)-1]
    # print(url_for('lteBlueprint.detailMax'))
    return render_template('lte/detailMax.html', maxAllField=maxAllField,maxAllRecord=maxAllRecord, p=pager, tableName=tableName)

@lteBlueprint.route('/lteCategories/detailMin/<tableName>')
def detailMin(tableName):
    page = request.args.get('p', 1)
    limit = request.args.get('limit', 9)
    offset = (int(page)-1) * int(limit)

    minAllRecord = SQLHelper.getMinAllRecord(connect_db(), tableName)[1]
    minAllField = SQLHelper.getMinAllRecord(connect_db(), tableName)[0]
    print('minAllRecord:',minAllRecord)
    total = len(minAllRecord)
    pager = {'total':int(total), 'limit':int(limit), 'curr_page':int(page)}
    minAllRecord = minAllRecord[int(offset):int(offset)+int(limit)-1]
    return render_template('lte/detailMin.html', minAllField=minAllField,minAllRecord=minAllRecord, p=pager, tableName=tableName)

