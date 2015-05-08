# -*- coding:utf-8 -*-
from datetime import datetime
import xlrd

def importxls(conn, filename):
    bk = xlrd.open_workbook(filename)

    with conn.cursor() as cur:
        try:
            for sheetName in bk._sheet_names()[1:]:
            #其中Index从第二行开始，其他从第六行开始作为数据插入
                if sheetName == 'Index':
                    tableExclude = []
                    newSheetName = 'TableIndex'
                elif sheetName == 'ParaTemplate':
                    tableExclude = []
                    newSheetName = sheetName
                else:
                    tableExclude = range(1,5)
                    newSheetName = sheetName

                sh = bk.sheet_by_name(sheetName)
                nrows = sh.nrows

                for row in range(0, nrows):
                    rowValue = map(lambda var:var+' varchar(128)', sh.row_values(row))
                    if row == 0:
                        sql = 'create table %s (id int not null auto_increment,' \
                              'availabe varchar(128), assetdate date, %s, primary key(id))' \
                              %(newSheetName, ','.join(sh.row_values(row)))
                        cur.execute(sql)
                    elif row in tableExclude:
                        pass
                    else:
                        assetValues = []
                        for i in sh.row_values(row):
                            if len(str(i))>255:
                                assetValues.append("")
                            else:
                                assetValues.append(str(i))
                        sql = 'insert into %s (availabe, assetdate, %s) values ("keeping", "%s","%s")'\
                                  %(newSheetName,','.join(sh.row_values(row)),str(datetime.now().date()), '","'.join(assetValues))
                            # print(sheet_name)
                        cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)