# coding=utf-8
from websocket_server import WebsocketServer
from RawSql import *
import json
import time
import os
import django
import threading
os.environ.setdefault('DJANGO_SETTING_MODULE', 'freechat.settings')
django.setup()


class MessagePush (threading.Thread):
    def __init__(self, client, server, message):
        threading.Thread.__init__(self)
        self.client = client
        self.server = server
        self.message = message

    def run(self):
        sql = "select stop from thread_manage where id=%s and stop=1" % (self.client['id'])
        raw = RawSql()
        while True:
            received_msg(self.client, self.server, self.message)
            stop = raw.get_json(sql)
            if stop:
                sql = "delete from thread_manage where id=%s" % self.client['id']
                raw.excute(sql)
                print("%s清理线程完毕" % self.client['id'])
                print("退出线程")
                exit()
            time.sleep(1)


def received_msg(client, server, message):
    raw = RawSql()
    sql = "update %s set read=-1 where read=0" % message['sender']
    raw.excute(sql)
    sql = "select * from %s where username='%s' and read=-1" % (message['sender'], message['receiver'])
    data = raw.get_json(sql)
    if data:
        server.send_message(client, data.replace("None", '""'))
        sql = "update %s set read=1 where read=-1" % message['sender']
        raw.excute(sql)


def new_client(client, server):
    print("Client(%d) has joined." % client['id'])


def client_left(client, server):
    raw = RawSql()
    sql = "update thread_manage set stop=1 where id=%s" % client['id']
    raw.excute(sql)


def message_back(client, server, message):
    data = bytes.decode(base64.b64decode(str.encode(message)))
    json_data = json.loads(data)
    if "content" not in json_data.keys():
        raw = RawSql()
        update_sql = "update %s set read=1 where username='%s'" % (json_data["sender"], json_data["receiver"])
        raw.excute(update_sql)
        t_handle = MessagePush(client, server, json_data)
        t_handle.start()
        sql = "insert into thread_manage(id, stop, ip) values ('%s', '%s', '%s')" % (client["id"], '0', client['address'][0])
        raw.excute(sql)
    else:
        content = bytes.decode(base64.b64encode(str.encode(json_data["content"])))
        send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sender_sql = "insert into %s(time, type, username, content, read) values ('%s', '%s', '%s', '%s', %s)" % (json_data["sender"], send_time, '0', json_data["receiver"], content, '1')
        receiver_sql = "insert into %s(time, type, username, content, read) values ('%s', '%s', '%s', '%s', %s)" % (json_data["receiver"], send_time, '1', json_data["sender"], content, '0')
        raw = RawSql()
        raw.excute(sender_sql)
        raw.excute(receiver_sql)
        server.send_message(client, '[{"status": "01", "time":"' + send_time + '"}]')


server = WebsocketServer(4200, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_back)
server.run_forever()
