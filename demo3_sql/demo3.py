import os
from flask import  Flask
from flask_sqlalchemy import  SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# 配置数据库地址
# app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql://root:admin@10.10.10.103:3306/flask_sql_demo'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 动态跟踪数据库的修改 -> 不建议修改，未来版本会删除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
两张表
角色（管理员/普通用户）
用户（角色ID）
'''

# 数据库的模型，需要继承自 db.Model
class Role(db.Model):
    # 定义表
    __tablename__ = 'roles'

    # 定义字段 db.column 表示是一个字段
    id = db.Column(db.Integer, primary_key=True)
    # name 要求唯一， 不能同时出现两个“管理员”
    name = db.Column(db.String(16), unique=True)
    # 表示和User模型关联，增加一个 users 属性
    # backref='role' 表示role是User要用的属性
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role: %s %s>' %(self.name, self.id)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    # db.ForeignKey('roles.id') 表示是外键。  表名.id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # User希望有role属性，但是这个属性的定义，需要在另一个模型中定义

    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __repr__(self):
        return '<User: %s %s %s %s' %(self.name, self.id, self.email , self.password)


@app.route('/')
def index():
    pass

if __name__ == '__main__':
    # 删除表
    db.drop_all()
    # 创建表
    db.create_all()

    ro1=Role(name='admin')
    db.session.add(ro1)
    db.session.commit()

    ro2=Role(name='user')
    db.session.add(ro2)
    db.session.commit()

    us1 = User(name='wang', email='wanggag@163.com', password='123456',role_id=ro1.id)
    us2 = User(name='zhang', email='wanagasg@163.com', password='123456',role_id=ro2.id)
    us3 = User(name='chen', email='wangagasg@163.com', password='123456',role_id=ro1.id)
    us4 = User(name='zhou', email='wangagasgg@163.com', password='123456',role_id=ro2.id)
    us5 = User(name='tang', email='wangagareg@163.com', password='123456',role_id=ro1.id)
    us6 = User(name='wu', email='wanagsgag@163.com', password='123456',role_id=ro2.id)
    us7 = User(name='qian', email='wangagag@163.com', password='123456',role_id=ro1.id)
    us8 = User(name='sin', email='wanggatg@163.com', password='123456',role_id=ro2.id)
    us9 = User(name='wg', email='wangfs@163.com', password='123456',role_id=ro1.id)
    us10 = User(name='ang', email='wasfsng@163.com', password='123456',role_id=ro1.id)
    db.session.add_all([us1,us2,us3,us4,us5,us6,us7,us8,us9,us10])
    db.session.commit()
    app.run()

"""
完成以下查询
1 查询所有用户数据
    User.query.all()
2 查询有多少用户
    User.query.count()
3 产需第一个用户
    User.query.first()
4 查询id是4的用户
    User.query.get(4)
    User.query.filter_by(id=4).first()
    User.query.filter(User.id==4).first()
    
    总结：
    filter_by：属性=**
    filter ： 对象.属性=**
    filter 功能更加强大，可以实现更多的查询条件，支持比较运算符，查询字符串（首字母结尾，包含 等，自己搜集下资料）
"""