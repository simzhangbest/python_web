import os
from flask import Flask, render_template,flash,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import data_required
app = Flask(__name__)


app.secret_key='simzhang'
'''
1、配置数据哭
    a 导入 库
    b 创建db
    c 终端创建数据库
2、添加书 和  作者的模型
    a 模型集成db.Model
    b __tablename__: 表名
    c db.Column:字段
    d db.relationship : 关系引用
3、添加数据
4、使用模板显示数据库查询的数据
    a 查询所有的作者的信息，让信息传递给模板
    b 模板中按照格式，依次for循环 作者和书籍(作者获取书籍，用的是关系引用)
5、使用wtf表单
    a 自定义表单类
    b 模板中显示 
    c secret_key / 编码问题 / csrf_token 问题
6、实现增删逻辑
    a 增加数据
    b 删除书籍  --> 网页中删除--> 点击需要发送书籍的id给删除书籍的路由 --> 路由需要接受参数
'''

basedir = os.path.abspath(os.path.dirname(__file__))
# 配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'books.sqlite')
# 动态跟踪数据库的修改 -> 不建议修改，未来版本会删除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# 定义书和作者模型
# 作者模型
class Author(db.Model):
    # 表名
    __tablename__ = 'authors'
    # 字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 关系引用
    # books 是 给自己用的， author 是给模型用的
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author: %s ' %self.name

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book: %s %s'%(self.name, self.author_id)

# 自定义表单类
class AuthorFrom(FlaskForm):
    author = StringField('作者：', validators=[data_required()])
    book = StringField('书籍：', validators=[data_required()])
    submit = SubmitField('提交')


@app.route('/delete_book/<book_id>')
def delte_book(book_id):
    #查询数据库是否有该id的数据，有就删除，没有就提示错误

    # 返回当前的网址，重定向
    # url_for 需要传入视图函数名，返回视图函数对应路由
    return redirect(url_for('index'))

@app.route('/', methods=['GET','POST'])
def index():
    # 创建自定义的表单类
    author_form = AuthorFrom()

    '''
    验证逻辑：
    1、 调用wtf验证函数
    2、 验证通过获取数据
    3、 判断作者是否存在
    4、 如果作者存在，判断书籍是否存在，没有重复书籍就添加数据，如果存在就提示错误
    5、 如果作者不存在，添加作者和书籍
    6、 验证不通过就提示错误
    '''
    # 1、调用wtf的函数实现验证
    if author_form.validate_on_submit():
        # 2、验证通过获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data

        # 3、判断作者是否存在
        author = Author.query.filter_by(name=author_name).first()
        # 4、 如果作者存在
        if author:
            #  判断书籍是否存在，没有重复书籍就添加数据，如果重复，就提示错误
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash('已存在同名书籍')
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('添加书籍失败')
                    db.session.rollback()
        else:
            # 5、 如果作者不存在，添加作者和书籍
            try:
                new_author=Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()
                new_book=Book(name=book_name,author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('添加作者书籍失败')
                db.session.rollback()
    else:
        # 6、验证不通过，提示错误
        if request.method == 'POST':
            flash('参数不全')

    # 查询作者的信息，让信息传递给模板
    authors = Author.query.all()
    return render_template('books.html', authors=authors, form=author_form)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老惠')
    au3 = Author(name='老刘')

    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    # 把数据提交给用户会话
    bk1 = Book(name='老万的会议',author_id = au1.id)
    bk2 = Book(name='老gg会议', author_id = au2.id)
    bk3 = Book(name='老saf会议', author_id = au3.id)
    bk4 = Book(name='老万nn会议', author_id = au1.id)
    bk5 = Book(name='老fuck的会议', author_id = au3.id)

    # 提交会话
    db.session.add_all([bk1,bk2,bk3,bk4,bk5])

    db.session.commit()
    app.run(debug=True)