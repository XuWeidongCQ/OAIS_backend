from flask import Flask
from flask_sockets import Sockets
from flask_socketio import SocketIO, send
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

# socketio = SocketIO(app)
#
#
# @socketio.on('connect',namespace='/ws/new_ope')
# def handle_connect():
#     print('ws连接成功')
#     # while True:
#     new_ope_num = 0
#     send(new_ope_num)
#     socketio.sleep(2)
#
# @socketio.on('disconnect',namespace='/ws/new_ope')
# def handle_disconnect():
#     print('ws断开连接')
#
# @socketio.on('message')
# def handle_message(msg):
#     print(msg)



@sockets.route('/ws/new_ope')
def send_new_ope(ws):
    print('建立ws连接---')
    new_ope_num = 0
    if ws.closed:
        print('请求关闭ws')
    while not ws.closed:
        print('发送数据'+str(new_ope_num)+str(ws.closed))
        # r_data = ws.receive()
        # if r_data is None:
        #     break
        if ws.closed:
            break
        try:
            ws.send(str(new_ope_num))
            time.sleep(100)
        except Exception as e:
            print('用户断开了连接')
            break
    return '完毕'

if  __name__ == '__main__':
    print('ws服务启动')
    # socketio.run(app,host='0.0.0.0',port=5001)
    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app, handler_class=WebSocketHandler)
    server.serve_forever()