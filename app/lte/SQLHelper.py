# -*- coding:utf-8 -*-
# from .. import mysql
from datetime import datetime
import xlrd
from collections import Counter

#导入中兴网规网优数据
def importxls(conn, filename):
    bk = xlrd.open_workbook(filename)

    with conn.cursor() as cur:
        try:
            for sheetName in bk.sheet_names()[1:]:
            #其中Index从第二行开始，其他从第六行开始作为数据插入
                if sheetName == 'Index':
                    tableExclude = []
                    newSheetName = 'TableIndex'
                elif sheetName == 'ParaTemplate':
                    tableExclude = []
                    newSheetName = sheetName
                else:
                    tableExclude = range(1, 5)
                    newSheetName = sheetName

                sh = bk.sheet_by_name(sheetName)
                nrows = sh.nrows

                #表配置文件
                sql = 'create table %s (id int not null auto_increment, tableField varchar(128)' \
                      ', status varchar(128) null default "", primary key(id))' %(newSheetName + '_Profile')
                # print(sql)
                cur.execute(sql)

                for row in range(0, nrows):
                    rowValue = map(lambda var:var+' varchar(128)', sh.row_values(row))
                    if row == 0:
                        tableValue = sh.row_values(row)
                        sql = 'create table %s (id int not null auto_increment,' \
                              'availabe varchar(128), assetdate date, %s, primary key(id))' \
                              %(newSheetName, ','.join(rowValue))

                        cur.execute(sql)
                        for i in sh.row_values(row):
                            sql = 'insert into %s (tableField) values ("%s")' \
                                  %(newSheetName+'_Profile', str(i))
                            cur.execute(sql)
                    elif row in tableExclude:
                        pass
                    else:
                        assetValues = []
                        #处理掉不合理值
                        for i in sh.row_values(row):
                            if len(str(i))>255:
                                assetValues.append("")
                            else:
                                assetValues.append(str(i))
                        sql = 'insert into %s (availabe, assetdate, %s) values ("working", "%s","%s")'\
                                  % (newSheetName, ','.join(tableValue), str(datetime.now().date()), '","'.join(assetValues))
                        cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)


#获得数据库所有表
def getAllTableNames(conn):
    with conn.cursor() as cur:
        tableNames = []
        sql = 'select * from TableIndex'
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tableNames.append(row[4])
        return tableNames

#获得指定表所有字段
def getTableFields(conn, tableName):
    with conn.cursor() as cur:
        tableValues = []
        sql = "select tableField from %s" % (tableName+'_Profile')
        # print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        # print(result)
        for row in result:
            tableValues.append(row[0])
        return tableValues

#获取状态为working的配置
def getWorkingField(conn, tableName):
    with conn.cursor() as cur:
        workingFields = []
        sql = "select tableField from %s where status='working'" % (tableName+'_Profile')
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            workingFields.append(row[0])
        print(workingFields)
        return workingFields

#更新配置文件
def updateProfile(conn, tableName, profileValues):
    with conn.cursor() as cur:
        sql = 'update %s set status="stop"' % (tableName+'_Profile')
        cur.execute(sql)
        for row in profileValues:
            sql = 'update %s set status="working" where tableField="%s"' %(tableName+'_Profile', row)
            cur.execute(sql)
        conn.commit()


#获得最大记录数
def getMaxRecord(conn, tableName):
    with conn.cursor() as cur:
        workingFields = getWorkingField(conn, tableName)
        sql = 'select %s from %s' %(','.join(workingFields), tableName)
        cur.execute(sql)
        result = cur.fetchall()
        workingValues = sorted(Counter(result),key=lambda k:Counter(result)[k], reverse=True)
        maxCount = Counter(result)[workingValues[0]]
        return [maxCount, workingValues[0]]

        # sqlCondition = ' and '.join(map(lambda x, y:x+"='"+y+"'", workingFields, workingCount[0]))
        # sql = "select {} from {} where {}".format(','.join(workingFields), tableName, sqlCondition)
        # cur.execute(sql)

#获得其他记录数
def getMinRecord(conn, tableName):
    with conn.cursor() as cur:
        sql = 'select count(*) from %s' % tableName
        cur.execute(sql)
        result = cur.fetchall()
        totalCount = result[0][0]
        print(totalCount,':',type(totalCount))
        minCount = totalCount-getMaxRecord(conn, tableName)[0]
        return minCount

#获得最大详细记录
def getMaxAllRecord(conn, tableName):
    with conn.cursor() as cur:
        maxAllRecord = []
        workingFields = getWorkingField(conn, tableName)
        workingValues = getMaxRecord(conn, tableName)[1]
        sqlCondition = ' and '.join(map(lambda x, y:x+"='"+y+"'", workingFields, workingValues))
        workingFields.insert(0, 'ENBFunctionFDD')
        sql = "select {} from {} where {}".format(','.join(workingFields), tableName, sqlCondition)
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            maxAllRecord.append(row)
        return [workingFields, maxAllRecord]

#获得其他详细记录
def getMinAllRecord(conn, tableName):
    with conn.cursor() as cur:
        minAllRecord = []
        workingFields = getWorkingField(conn, tableName)
        workingValues = getMaxRecord(conn, tableName)[1]
        sqlCondition = ' or '.join(map(lambda x, y:x+"!='"+y+"'", workingFields, workingValues))
        workingFields.insert(0, 'ENBFunctionFDD')
        sql = "select {} from {} where {}".format(','.join(workingFields), tableName, sqlCondition)
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            minAllRecord.append(row)
        return [workingFields, minAllRecord]


