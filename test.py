import pymysql

conn = pymysql.connect(host='172.24.216.191', user='book_manager', password='fan123', db='book_manager', charset='utf8')


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


sql = 'select _id,from borrow'
c = query_sql(sql)[0][3]
print(c)
