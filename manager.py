from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from istock import create_app

# 调用方法,获取app
app = create_app("develop")

# 创建应用程序管理对象
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
