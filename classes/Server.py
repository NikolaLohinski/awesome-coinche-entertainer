import json
import os.path
from tornado import ioloop, web, websocket

from classes.Manager import Manager

_DEFAULT_PORT_ = 8080

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), '..', 'out'),
    static_path=os.path.join(os.path.dirname(__file__), '..', 'out'),
)


class RootServer(web.RequestHandler):
    def get(self):
        self.render('index.html')


class WSHandler(websocket.WebSocketHandler):
    """Tornado websocket handler"""

    def __init__(self, *args, manager, **kwargs):
        super(WSHandler, self).__init__(*args, **kwargs)
        self.manager = manager

    def open(self):
        """Called when a socket is opened."""

    def on_message(self, message):
        """Called when a socket transmitted a message."""
        action = json.loads(message)
        head = action.get('H')
        body = action.get('B')
        try:
            result = self.respond(head=head, body=body)
            for r in result:
                ws_handler, message = r
                self.send(message=message, handler=ws_handler)
        except Exception as err:
            self.send(message={'H': 'ERROR', 'B': err.args}, handler=self)

    def on_close(self):
        """Called when a socket is closed."""

    def send(self, message, handler):
        handler.write_message(json.dumps(message))

    def respond(self, head, body):
        if head == 'CREATE':
            return self.manager.create(socket=self, args=body)
        elif head == 'JOIN':
            return self.manager.join(socket=self, args=body)
        elif head == 'UPDATE':
            return self.manager.update(args=body)
        elif head == 'QUIT':
            return self.manager.quit(args=body)
        elif head == 'RESTART':
            return self.manager.restart(socket=self, args=body)
        elif head == 'START':
            return self.manager.start(args=body)
        elif head == 'ALIVE':
            return []
        else:
            raise Exception('badRequest')


def main(port=_DEFAULT_PORT_):
    manager = Manager()
    app = web.Application([
        (r'/ws', WSHandler, dict(manager=manager)),
        (r'/', RootServer),
        (r'/reach', RootServer),
        (r'/(.*)', web.StaticFileHandler, {
            'path': './out'
        }),
    ], **settings)
    app.listen(port)
    print('Initialized on http://localhost:{}/'.format(port))
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    settings['debug'] = True
    main()
