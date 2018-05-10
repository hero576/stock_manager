from flask import Blueprint, current_app
from flask_wtf.csrf import generate_csrf

# 创建蓝图
html = Blueprint("web_html", __name__)


# 使用蓝图装饰视图函数
@html.route("/<re(r'.*'):file_name>")
def get_html_page(file_name):
    # 判断是否是访问的根路径, 如果是根路径,拼接index.html
    if not file_name:
        file_name = "index.html"
    print(file_name)
    # 判断不是favicon.ico才进行拼接
    if file_name != "favicon.ico":
        file_name = "html/" + file_name

    respone = current_app.send_static_file(file_name)
    # 给cookie中设置csrf_token
    token = generate_csrf()
    respone.set_cookie("csrf_token", token)

    return respone
