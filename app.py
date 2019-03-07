# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from utils.mysql_db import *
from utils.config import *

app = Flask(__name__)
mysql_conn = DB(host=TestConfig.MYSQL_HOST, port=TestConfig.MYSQL_PORT, user=TestConfig.MYSQL_USER,
                         password=TestConfig.MYSQL_PASSWORD, db=TestConfig.MYSQL_DB)
def get_gifs(mysql_conn,text):
    cursor = mysql_conn.get_cursor()
    sql = "select guid from `weshine-text` where text='%s'"%text
    print sql
    cursor.execute(sql)
    rs=cursor.fetchall()
    if len(rs)==0:
        tmp_str = u"'%{}%'".format(text)
        sql = "select text from `weshine-text` where text like " +tmp_str
        print sql
        cursor.execute(sql)
        rs = cursor.fetchall()
        if len(rs)==0:
            return "No result"
        text_list = []
        for r in rs:
            text_list.append(r[0])
        return {"text_list":text_list}

    text_guid=rs[0][0]
    sql_2 = "select pic_guid from `weshine-text-pic` where text_guid='%s'"%text_guid
    cursor.execute(sql_2)
    pic_guids=cursor.fetchall()
    if len(pic_guids)==0:
        return "No result"
    pic_guid_list=[]
    for pic in pic_guids:
        pic_guid_list.append("'%s'"%pic[0])

    query_str = ",".join(pic_guid_list)
    sql_3 = "select big_url from `weshine-pic` where guid in ("+query_str+");"
    print sql_3
    cursor.execute(sql_3)
    url_rets=cursor.fetchall()
    if len(url_rets)==0:
        return "No result"
    url_list = []
    for url in url_rets:
        url_list.append(url[0])
    return url_list


@app.route('/search',methods=["GET"])
def search_gifs():
    text = request.values.get("text")
    if text is None:
        return jsonify(code=1,result="query param cannot be empty!",error="")
    try:
        rets = get_gifs(mysql_conn, text)

    except Exception as e:
        return jsonify(code=1,result="",error="server error")
    return jsonify(code=0,result=rets,error="")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8848)