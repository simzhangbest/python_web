from flask import  Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    url_str = 'www.baidu.com'

    my_list = [1,3,4,7,5]

    my_dict = {
        "name":"simzhng",
        "url":"www.baidu.com"
    }

    my_int = 33
    # 通常 模板中使用的变量名和要传递的数据名 保持一致
    return render_template('index.html', url_str=url_str, my_list=my_list, my_dict = my_dict, my_int = my_int)

if __name__ == '__main__':
    app.run(debug=True)