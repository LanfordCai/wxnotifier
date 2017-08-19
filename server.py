# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.web
import itchat
import threading
import global_variables


class WechatMsgHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/x-www-form-urlencoded")
        msg = self.get_body_argument("msg")
        if msg != None:
            if global_variables.target_room is not None:
                print("send!")
                itchat.send(msg, global_variables.target_room["UserName"])
            else:
                print("target_room is None")
        else:
            print("msg is None")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, wxnotifier")

def prepareWechat():
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    rooms = itchat.get_chatrooms()
    print(len(rooms))
    for r in rooms:
        if r['NickName'] == u'币推送':
            global_variables.target_room = r
            print("tareget room is %s" % global_variables.target_room["UserName"])
            break
    itchat.run()


if __name__ == "__main__":
    print("PrepareWechat")
    t = threading.Thread(target=prepareWechat, name="Wechat")
    t.start()
    print("Go!")
    app = tornado.web.Application(handlers=[(r'/wechat', WechatMsgHandler), (r'/', IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8765)
    tornado.ioloop.IOLoop.instance().start()
