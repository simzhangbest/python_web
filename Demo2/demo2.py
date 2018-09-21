from flask import  Flask, render_template, request, flash
from  flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.secret_key = "simzhang"

# 实现简单的登录逻辑处理
#   1、路由需要有get 和 post
#   2、获取请求的参数
#   3、判断参数是否填写 && 密码是否相同
#   4、如果判断没问题，就返回一个sussess 表示成功

# 给模板传递消息
# flash --> 需要对内容加密，因此需要设置secret_key,做加密消息
# 模板需要遍历消息

'''
使用wtf 实现表单
自定义表单类
'''
class LoginForm(FlaskForm):
    username = StringField('用户名:', validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    password2 = PasswordField('确认密码:', validators=[DataRequired(), EqualTo('password', '密码填入不一致')])
    submit = SubmitField('提交')

'''
WTF 验证函数
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # 1 判断请求方式
    if request.method == 'POST':
    # 2 获取请求参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
    # 3 验证参数 wtf可以一句话实现所有的参数校验
    #   代码没错，但是缺少了csrf token
    if login_form.validate_on_submit():
        print(username, password)
        return 'success'
    else:
        flash("参数有误")
    return render_template('index.html', my_form = login_form)

@app.route('/', methods=['GET', 'POST'])
def index():
    #  request 请求对象， ---> 获取请求方式和数据
    if request.method == 'POST':
        # 2 通过request 获取 请求参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # print(username, password, password2)
        # 3 验证
        if not all([username, password, password2]):
            # print("missing params")
            flash("参数缺失")
        elif password != password2:
            # print("password not match")
            flash("两次密码不一致")
        else:
            return 'success'

    return  render_template('index.html')

if __name__ == "__main__":
    app.run()

