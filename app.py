from flask import Flask, request, render_template, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
import pymysql.cursors
import time
import os
import socket
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = os.urandom(64)
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,  # 使用客户端IP作为限制的键
#     default_limits=["5 per minute"]  # 默认限制，每分钟最多5次请求
# )

# 等待数据库初始化上线
url = make_url("mysql+pymysql://root:sssctf2024_rootpassword@scr1wgpt-mysql/sssctf2024_db")
url.database = None
engine = create_engine(url)
print(f"等待数据库就绪。。。", end="", flush=True)
while True:
    try:
        engine.raw_connection()
        break
    except Exception:
        print("。", end="", flush=True)
        time.sleep(3)
print("", flush=True)

# MySQL 连接配置
conn = pymysql.connect(
    host='scr1wgpt-mysql',
    user='root',
    password='sssctf2024_rootpassword',
    database='sssctf2024_db',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
# @limiter.limit("10 per minute")  # Limits to 10 login attempts per minute
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        waf = ['or', 'and', '/', '0x', '0b', '0o', ';', 'outfile', 'load_file', 'terminated', 'field']
        ulow = username.lower()
        plow = password.lower()
        for waff in waf:
            if waff in ulow or waff in plow:
                msg = "Login failed!"
                return render_template('login.html', msg=msg)

        cur = conn.cursor()
        query = f"SELECT * FROM sssctf2024_users WHERE username='{username}' AND password='{password}' LIMIT 0,1"

        try:
            cur.execute(query)     # 执行SQL查询
            result = cur.fetchall()         # 获取所有结果
            if result:
                if not (username == 'Scr1w_admin' and password == 'sssctf2024_P@ssvv0rd'):
                    msg = 'Login failed!'
                    return render_template('login.html', msg=msg)

                session['username'] = username  # 将用户名存储在会话中
                return redirect(url_for('options'))
            else:
                msg = 'Login failed!'

        except Exception as error:
            print(f"An error occurred: {error}", flush=True)
            msg = 'Login failed!'

    return render_template('login.html', msg=msg)

@app.route('/options')
def options():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('options.html')

def get_scr1wgpt_ip():
    try:
        return socket.gethostbyname('scr1wgpt')
    except socket.gaierror:
        return None

@app.route('/generator')
def flag():
    scr1wgpt_ip = get_scr1wgpt_ip()
    if scr1wgpt_ip is None:
        return 'Unable to resolve scr1wgpt domain'
    if request.remote_addr != scr1wgpt_ip:
        return render_template('generator.html', message='Remote test flag has been generated:\nSsS(tF{f@k3_f|4g_l-lAl-lA]')
    flag_value = os.getenv('FLAG', 'Flag not set')
    return render_template('generator.html', message="Local flag has been generated:\n" + flag_value)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')

