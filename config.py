#coding:utf8
import redis
import logging

class BaseConfig(object):
    """启动配置类"""
    SECRET_KEY = "djfkdjfd"

    # #数据库配置
    # SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/flask_ihome"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # MongoDB配置
    MONGO_DB_HOST = "127.0.0.1"
    MONGO_DB_PORT = 27017


    # #sessioin配置
    SESSION_TYPE = "redis"#指定session的保存位置
    SESSION_USE_SIGNER = True #设置sessioin存储签名
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 24*3600 *2 #session的有效时间,单位秒

class Developer(BaseConfig):
    """开发模式"""
    DEBUG = True
    #开发的时候是DEBUG级别
    DEBUG_LEVEL = logging.DEBUG


class Production(BaseConfig):
    """生成环境"""
    #生产环境是ERROR级别
    DEBUG_LEVEL = logging.ERROR
    pass

#提供外界获取配置信息方式
config_dict = {
    "develop": Developer,
    "product": Production
}
