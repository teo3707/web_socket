# coding: utf-8
import json
import time
import datetime
import tornado.websocket
from status.models import *


class Channel:

    def __init__(self):
        self.items = []     # [webSocket, ..]
        self.status_list = []

    def notify(self, message):
        for item in self.items:
            item.write_message(message)

    def add(self, item):
        self.items.append(item)

    def update_status(self, key, status, binding=None):
        self.status_list.append([status, binding])
        model = Status()
        model.key = key
        model.status = status
        model.binding = binding
        model.create_time = time.strftime("%Y%m%d%H%M%S", datetime.datetime.now().timetuple())
        model.save()


class Socket(tornado.websocket.WebSocketHandler):

    _channels = {}

    def check_origin(self, origin):
        return True

    def open(self):
        # self.write_message("open success")
        pass

    def on_message(self, json_str):
        message = json.loads(json_str, encoding="utf-8")
        t = message['type']   # `type` cannot be null
        key = message['key']  # `key` cannot be null
        setattr(self, "key", key)

        status = message['status'] if 'status' in message else None
        binding = message['binding'] if 'binding' in message else None

        if t == 'subscribe':  # create channel if not exist and send status to client
            channel = None
            if key in Socket._channels:
                channel = Socket._channels[key]
            else:
                channel = Channel()
                channel.add(self)
                Socket._channels[key] = channel

            channel.add(self)
            if status and not len(channel.status_list):
                channel.update_status(key, status, binding)
            else:
                try:
                    self.write_message(json.dumps({'key': key, 'status': channel.status_list}))
                except:
                    pass

        elif t == "updateStatus":
            channel = Socket._channels[key]
            channel.update_status(key, status, binding)

            is_last_status = message['isLastStatus'] if 'isLastStatus' in message else None
            channel = Socket._channels[key]
            for item in channel.items:
                try:
                    item.write_message(json.dumps({'key': key, 'status': channel.status_list}))
                except:
                    pass

                if is_last_status:
                    try:
                        item.close()
                    except:
                        pass
            if is_last_status:
                del Socket._channels[key]
