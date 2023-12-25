from threading import Thread
from time import sleep

from gpiozero import LED
import board
import adafruit_dht


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


class SensorPlugin:
    """
    circuit:
    dht11 pins left to right:
        (1) signal -> GPIO (pin7) => board.Dx where x => GPIO number
        (2) VCC -> 5Volt (pin2)
        (3) negativ -> Ground (pin6)

    """
    def __init__(self, app):
        self.device = adafruit_dht.DHT11(board.D4, use_pulseio=False)
        self.humidity = 0.0
        self.temperature = 0.0
        # dhtDevice.exit()
 
    def update(self):
        self.temperature = self.device.temperature
        self.humidity = self.device.humidity

    def exit(self):
        self.device.exit()


    def get_climate(self):
        return template('<h1>current climate</h1><h2>Temperature: {{temp}}° </h2><h2>Humidity:{{ hum }} %</h2>', temp=self.temperature, hum=self.humidity)


    def init_routes(self):
        endpoint = '/sensor'
        routes = [
                ("/climate", "GET", self.get_climate)
            ]

        return endpoint, routes




class LedPlugin:
    def __init__(self, app):
        self.led = LED(14)
        self.led_on = False
    
    def toggle_light(self):
        self.led_on = not self.led_on
        return template('<h1>Light is on?{{ status }} </h1>', status=self.led_on)
    
    def init_routes(self):
        endpoint = '/led'
        routes = [
                ("/toggle", "GET", self.toggle_light)
            ]

        return endpoint, routes


    def update(self):
        if self.led_on:
            self.led.on()
        else:
            self.led.off()

PLUGINS = [
        LedPlugin,
        SensorPlugin
        ]

class App:
    running = False
    plugins = []

    def __init__(self):
        self.server = Server(self)
    

    def _init_server(self):
        self.server_thread = Thread(target=self.run_server, name="server")
        self.server_thread.deamon = True
        self.server_thread.start()

    
    def start(self):
        self.is_running = True
        self._init_server()
        self._init_plugins()
        # always init plugins first so their routes can be gathered
        self._init_routes()


    def _init_plugins(self):
        for plugin_cls in PLUGINS:
            plugin = plugin_cls(self)
            self.plugins.append(plugin)

    def _init_routes(self):
        for plugin in self.plugins:
            endpoint, plugin_routes = plugin.init_routes()
            for (_rule, http_method, callback) in plugin_routes:
                rule = endpoint + _rule
                print(f'adding route {rule} [{http_method}]')
                self.server.add_route(rule, http_method, callback)
            

    def run_server(self):
        print(f'starting server on {self.server._HOST}:{self.server._PORT}')
        bottle_run(self.server, host=self.server._HOST,port=self.server._PORT)


    def exit(self):
        self.server_thread.join()
        print(f'shutting down')

        
    def update(self):
        for plugin in self.plugins:
            plugin.update()

if __name__ == '__main__':
    app = App()
    app.start()
    while True:
        try:
            app.update()
        except KeyboardInterrupt:
            app.exit()
            exit(0)

