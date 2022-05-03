from flask import Flask, template_rendered, render_template, request
import pymysql

app = Flask(__name__)

conn = pymysql.connect(
    host='172.30.79.15',
    user='book_manager',
    password='fan123',
    db='book_manager',
    charset='utf8'
)


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
            cur = conn.cursor()
            sql = 'select book._id,name,author,press,cls_name from book,book_cls where cls=book_cls._id and active=1 order by _id'
            cur.execute(sql)
            content = cur.fetchall()
            return render_template('main.html', content=content)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    match request.method:
        case 'GET':
            cur = conn.cursor()
            sql = 'select book._id,name,author,press,cls_name,active from book,book_cls where cls=book_cls._id order by _id'
            cur.execute(sql)
            content = cur.fetchall()
            return render_template('admin.html', content=content)


def excute_sql(sql, args=tuple()):
    with conn.cursor() as cur:
        if len(args) > 0:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        flag = cur.rowcount
        conn.commit()
    return flag


@app.route('/control', methods=['GET', 'POST'])
def control():
    cmd = request.values.get('cmd')
    book_id = request.values.get('book_id')
    match cmd:
        case 'down_store':
            sql = 'update book set active = 0 where _id = %s'
            flag = excute_sql(sql, (book_id,))
            if flag:
                return render_template('success.html', message='下架')
        case 'up_store':
            sql = 'update book set active = 1 where _id = %s'
            flag = excute_sql(sql, (book_id,))
            if flag:
                return render_template('success.html', message='上架')
        case 'del_book':
            sql = 'delete from book where _id=%s'
            flag = excute_sql(sql, (book_id,))
            if flag:
                return render_template('success.html', message='删除')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    pass


@app.route('/update_book', methods=['GET', 'POST'])
def update_book():
    pass


if __name__ == '__main__':
    app.run()
