from threading import Thread
from time import sleep

from gpiozero import LED

from bottle import Bottle, Route, template
from bottle import run as bottle_run



class Server(Bottle):
    _PORT = 1337
    _HOST = '0.0.0.0'

    def __init__(self, app):
        self.app = app
        super().__init__()


    def add_route(self, rule, http_method, callback):
        route = Route(self, rule, http_method, callback)
        super().add_route(route)

class App:
    running = False

    def __init__(self):
        self.server = Server(self)
        self.led = LED(14)
        self.led_on = False
    
    def _init_server(self):
        self.server_thread = Thread(target=self.run_server, name="server")
        self.server_thread.deamon = True
        self.server_thread.start()

    def toggle_light(self):
        self.led_on = not self.led_on
        return template('<h1>Light is on?{{ status }} </h1>', status=self.led_on)
    
    def start(self):
        self.is_running = True
        self._init_server()
        self._make_routes()

    def _make_routes(self):
        r = ("/toggle", "GET", self.toggle_light)
        print(f'adding route {r}')
        self.server.add_route(*r)

    def run_server(self):
        print(f'starting server on {self.server._HOST}:{self.server._PORT}')
        bottle_run(self.server, host=self.server._HOST,port=self.server._PORT)

    def exit(self):
        self.server_thread.join()
        print(f'shutting down')

        
    def run(self):
        # for plugin in self plugins plugin run
        if self.led_on:
            self.led.on()
        else:
            self.led.off()

if __name__ == '__main__':
    app = App()
    app.start()
    while True:
        try:
            app.run()
        except KeyBoardInterupt:
            app.exit()
            exit(0)

