# coding:utf8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, session
from flask_session import Session  # 用来指定session存储的位置
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config_dict
import redis
from pymongo import MongoClient

# 创建数据库对象
from istock.utils.commons import RegexConverter


# #创建数据库对象
# db = SQLAlchemy()
#
#创建redis_stroe对象
redis_store = None;

#创建mongodb_stroe对象
mongodb_store = None;

# 工场方法,根据配置信息,返回对应的app对象
def create_app(config_name):
    # 创建应用程序对象
    app = Flask(__name__)

    # 通过配置名,获取到配置类
    config = config_dict.get(config_name)

    # 将配置信息加载到app中
    app.config.from_object(config)

    # 创建日志记录文件
    log_file(config.DEBUG_LEVEL)

    # 初始化session
    Session(app)

    # #初始化数据库,绑定数据库和应用程序app
    # db.init_app(app)

    # csrf配置
    # CSRFProtect(app)

    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    # 初始化mongodb
    global mongodb_store
    mongodb_store = MongoClient(host=config.MONGO_DB_HOST,port=config.MONGO_DB_PORT)

    # 添加自定义的转换器到转换器列表中
    app.url_map.converters["re"] = RegexConverter

    # 注册蓝图
    from istock.api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")

    # 注册静态文件蓝图
    from istock.web_html import html
    app.register_blueprint(html)

    print(app.url_map)
    return app


def log_file(debug_level):
    # 常见的日志等级如下: DEBUG < INFO <Waring < ERROR
    # 比如,如果等级设置为INFO那么,大于等于INFO级别的才会显示
    # 设置日志的记录等级
    logging.basicConfig(level=debug_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日记录器
    logging.getLogger().addHandler(file_log_handler)
