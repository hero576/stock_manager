# coding:utf8
import logging
import flask
from istock import mongodb_store
from . import api
from flask import current_app, render_template, jsonify,request
from stork_query import stock_check, result_parse, get_stock



@api.route('/', methods=["GET", "POST"])
def index():
    if flask.request.method == 'GET':
        result=[]
        page_num=request.args.get('p',1)
        print(request.url)
        print(request.args.get('p'))
        page_count=30

        collection = mongodb_store['stock']['stock']
        total_count=collection.find().count()
        total_page=int(total_count/page_count)

        if total_page>page_num:
            page_next=page_num+1
        else:
            page_next=None
        if page_num==1:
            page_per=None
        else:
            page_per=page_num+1

        if total_page<=5:
            page_list=[i+1 for i in range(total_page)]
        elif page_num<=2:
            page_list=[i+1 for i in range(5)]
        elif page_num>=total_page-2:
            page_list = [i + 1 for i in range(total_page-5,total_page)]
        else:
            page_list=[i + 1 for i in range(page_num-2,page_num+3)]
        skip=page_count*(page_num-1)
        ret=collection.find().limit(page_count).skip(skip)
        stock_id_list=[i['stock_id'] for i in ret]
        for stock_id in stock_id_list[0:30]:
            code = stock_check(stock_id)
            if code != 0:
                try:
                    result.append(result_parse(get_stock(code)))
                except:
                    continue
        print(page_list,page_num,page_next,total_page,page_per)
        return jsonify(errno='0', data='OK', result=result,page_list=page_list,page_per=page_per,page_next=page_next)
    elif flask.request.method == 'POST':
        stock_no = request.json['id']
        code = stock_check(stock_no)
        if code != 0:
            result = result_parse(get_stock(code))
            return jsonify(errno='0', data='OK', result=result)
        else:
            return jsonify(errno='1', data='OK', result="请输入正确的股票代码")
