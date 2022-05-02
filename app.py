from flask import Flask, template_rendered, render_template, request
import pymysql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    user_name = request.values.get('user_name')
    user_pwd = request.values.get('user_pwd')
    user_role = request.values.get('role')
    return f'{user_role} {user_name} 登录成功！'


@app.route('/register', methods=['GET', 'POST'])
def register():
    match request.method:
        case 'GET':
            return render_template('register.html')
        case 'POST':
            user_name = request.values.get('user_name')
            user_pwd = request.values.get('user_pwd')
            user_role = 'user'
            return f'{user_name} 注册成功！'


@app.route('/main', methods=['GET', 'POST'])
def main():
    match request.method:
        case 'GET':
            return render_template('main.html')
        case 'POST':
            sql='select book._id,name,author,press,cls_name,active from book,book_cls where cls=book_cls._id'
            


if __name__ == '__main__':
    app.run()
