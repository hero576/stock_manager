# coding:utf8
import configparser

import flask
from flask import render_template

from stork_query import stock_check, result_parse, get_stock

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if flask.request.method == 'GET':
        result = {}
        return render_template("istock/static/html/index.html", result=result)
    elif flask.request.method == 'POST'and flask.request.form.get('query', None) == "查询":
        stock_no = flask.request.form['storkcode']
        code = stock_check(stock_no)
        if code != 0:
            result = result_parse(get_stock(code))
            return render_template("istock/static/html/index.html", result=result)
        else:
            return render_template("istock/static/html/index.html", warning="请输入正确的股票代码")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=4501)