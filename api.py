from flask import Flask, g

from db import redis_client

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    """
    Opens a new redis connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'redisclient'):
        g.redisclient = redis_client()
    return g.redisclient


@app.route('/')
def index():
    return '<h2>hello,小马哥</h2>'


@app.route('/get')
def get_proxy():
    """
    Get a proxy
    """
    conn = get_conn()
    ip=conn.lget()
    conn.rput(ip)
    return ip


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    """
    conn = get_conn()
    return str(conn.lenth())
@app.route('/pop')
def pop_proxy():
    conn = get_conn()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
