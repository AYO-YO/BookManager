import pymysql
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

conn = pymysql.connect(host='172.19.201.172', user='book_manager', password='fan123', db='book_manager', charset='utf8')

user = {}


@app.route('/')
def index():
    return render_template('index.html')


def excute_sql(sql: str, args=tuple()) -> int:
    with conn.cursor() as cur:
        if len(args) > 0:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        flag = cur.rowcount
        conn.commit()
    return flag


def query_sql(sql, args=tuple()):
    with conn.cursor() as cur:
        if len(args) > 0:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        content = cur.fetchall()
        return content


@app.route('/login', methods=['POST'])
def login():
    user_name = request.values.get('user_name')
    user_pwd = request.values.get('user_pwd')
    user_role = 0 if request.values.get('role') == 'admin' else 1
    print(user_role)
    sql = 'select * from user where user_name=%s and user_pwd=%s and role=%s'
    flag = len(query_sql(sql, (user_name, user_pwd, user_role))) > 0
    print(flag)
    if flag:
        user['name'] = user_name
        return redirect(url_for('main' if user_role else 'admin'))
    else:
        return render_template('alert.html', t='验证失败！', m='请检查用户名或密码是否正确！')


@app.route('/register', methods=['GET', 'POST'])
def register():
    match request.method:
        case 'GET':
            return render_template('register.html')
        case 'POST':
            user_name = request.values.get('user_name')
            user_pwd = request.values.get('user_pwd')
            user_role = 1
            sql = 'select * from user where user_name=%s'
            flag = len(query_sql(sql, (user_name,))) > 0
            if flag:
                return render_template('alert.html', t='注册失败', m='用户名已存在！')
            sql = 'insert into user(user_name, user_pwd, role) values (%s,%s,%s)'
            flag = excute_sql(sql, (user_name, user_pwd, user_role))
            if flag:
                return render_template('alert.html', t='注册成功', m=f'{user_name}, 注册成功！')
            else:
                return render_template('alert.html', t='注册失败', m='注册失败，请联系管理员！')


@app.route('/main', methods=['GET', 'POST'])
def main():
    match request.method:
        case 'GET':
            cur = conn.cursor()
            sql = 'select book._id,name,author,press,cls_name from book,book_cls where cls=book_cls._id and active=1 ' \
                  'order by _id '
            cur.execute(sql)
            content = cur.fetchall()
            return render_template('main.html', content=content)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    match request.method:
        case 'GET':
            cur = conn.cursor()
            sql = 'select book._id,name,author,press,cls_name,active from book,book_cls where cls=book_cls._id order ' \
                  'by _id '
            cur.execute(sql)
            content = cur.fetchall()
            return render_template('admin.html', content=content)


@app.route('/control', methods=['GET', 'POST'])
def control():
    cmd = request.values.get('cmd')
    book_id = request.values.get('book_id')
    match cmd:
        case 'down_store':
            sql = 'update book set active = 0 where _id = %s'
            flag = excute_sql(sql, (book_id,))
            if flag:
                return render_template('alert.html', t='下架成功', m='下架成功')
        case 'up_store':
            sql = 'update book set active = 1 where _id = %s'
            flag = excute_sql(sql, (book_id,))
            if flag:
                return render_template('alert.html', t='上架成功', m='上架成功')
        case 'del_book':
            sql = 'delete from book where _id=%s'
            flag = excute_sql(sql, (book_id,))
            if flag:
                return render_template('alert.html', t='删除成功', m='删除成功！')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    match request.method:
        case 'GET':
            cls = query_sql('select cls_name from book_cls')
            return render_template('addbook.html', cls=cls)
        case 'POST':
            book_name = request.values.get('book_name')
            book_auth = request.values.get('book_auth')
            book_press = request.values.get('book_press')
            book_cls = request.values.get('book_cls')
            cls_id = query_sql('select _id from book_cls where cls_name = %s', (book_cls,))[0]
            is_active = request.values.get('is_active') == 'on'
            sql = 'insert into book (name, author, press, cls, active) values (%s, %s, %s, %s,%s)'
            flag = excute_sql(sql, (book_name, book_auth, book_press, cls_id, is_active)) > 0
            if flag:
                return render_template('alert.html', t='添加成功', m='添加成功！')


@app.route('/update_book', methods=['GET', 'POST'])
def update_book():
    match request.method:
        case 'GET':
            book_id = request.values.get('book_id')
            content = \
                query_sql(
                    'select book._id,name,author,press,cls_name,active from book,book_cls where cls=book_cls._id and '
                    'book._id=%s', (book_id,))[0]
            cls = query_sql('select cls_name from book_cls where cls_name!=%s', (content[4],))
            return render_template('update_book.html', content=content, cls=cls[1:])
        case 'POST':
            book_id = request.values.get('book_id')
            book_name = request.values.get('book_name')
            book_auth = request.values.get('book_auth')
            book_press = request.values.get('book_press')
            book_cls = request.values.get('book_cls')
            cls_id = query_sql('select _id from book_cls where cls_name = %s', (book_cls,))[0][0]
            is_active = 1 if request.values.get('is_active') == 'on' else 0
            sql = 'update book set name=%s,author=%s,press=%s,cls=%s,active=%s where _id=%s'
            print(book_name, book_auth, book_press, cls_id, is_active, book_id)
            flag = excute_sql(sql, (book_name, book_auth, book_press, cls_id, is_active, book_id)) > 0
            print(flag)
            if flag:
                return render_template('alert.html', t='修改成功', m='修改成功')
            else:
                return render_template('alert.html', t='修改', m='未修改数据！')


@app.route('/sub')
def sub():
    user_id = query_sql('select _id from user where user_name=%s', (user['name'],))[0]
    book_id = request.values.get('book_id')
    book_name = query_sql('select name from book where _id=%s', (book_id,))[0][0]
    # 是否已经借阅
    sql = 'select * from borrow where user_id=%s and book_id=%s and is_return=0'
    flag = len(query_sql(sql, (user_id, book_id))) > 0
    if flag:
        # 借阅失败，两种情况，一种是已经借了本种图书但没有归还
        return render_template('alert.html', t='借阅失败', m='借阅失败，请检查是否账户是否异常！')
    # 借阅
    sql = 'insert into borrow(user_id, book_id) VALUES (%s,%s)'
    flag = excute_sql(sql, (user_id, book_id)) > 0
    if flag:
        # 借阅成功
        return render_template('alert.html', t='借阅成功', m=f'借阅{book_name}成功！')
    else:
        # 另外一种（暂未实现）是用户所借图书已达上限
        return render_template('alert.html', t='借阅失败', m='借阅失败，请检查是否账户是否异常！')


if __name__ == '__main__':
    app.run()
