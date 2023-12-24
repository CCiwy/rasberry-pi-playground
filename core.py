class AppRoute:
    def __init__(self, rule, callback, http_method="GET", param=False):
        self.rule = rule
        self.callback = callback
        self.http_method = http_method
        self.param = self._set_param(param)



    def get(self):
        """ return the route data as called in endpoint.make_routes """
        rule = self.rule if not self.param else f'{self.rule}/{self.param}'
         
        return (self.http_method, rule, self.callback)
 

    def _set_param(self, param):
        if param and param.startswith('<') and param.endswith('>'):
            return param 
        
        return False


class BasePlugin:
    instances = {}
    endpoint = None

    def __init__(self, app, ident):
        self.app = app
        self.name = name
        self.instances[ident] = self
        self.endpoint = f'{name}/'
        
    def make_route(self, http_method, rule, callback, *args, **kwargs):
        route = AppRoute(rule, callback, http_method, *args, **kwargs)
