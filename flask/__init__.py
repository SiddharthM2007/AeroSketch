import json
from types import SimpleNamespace


class Request(SimpleNamespace):
    def get_json(self, silent=False):
        return getattr(self, 'json', None)


class Response:
    def __init__(self, data='', status=200, headers=None):
        self.data = data.encode() if isinstance(data, str) else data
        self.status_code = status
        self.headers = headers or {}

    def get_json(self):
        return json.loads(self.data.decode())


class Blueprint:
    def __init__(self, name, import_name):
        self.name = name
        self.import_name = import_name
        self.routes = []

    def route(self, rule, methods=None):
        methods = methods or ['GET']

        def decorator(func):
            self.routes.append((rule, [m.upper() for m in methods], func))
            return func

        return decorator


class Flask:
    def __init__(self, import_name, template_folder='templates'):
        self.import_name = import_name
        self.template_folder = template_folder
        self.routes = {}
        self.testing = False
        self.config = {}

    def register_blueprint(self, bp: Blueprint):
        for rule, methods, func in bp.routes:
            self.add_url_rule(rule, func, methods)

    def add_url_rule(self, rule, func, methods):
        self.routes.setdefault(rule, {})
        for m in methods:
            self.routes[rule][m] = func

    def route(self, rule, methods=None):
        methods = methods or ['GET']

        def decorator(func):
            self.add_url_rule(rule, func, [m.upper() for m in methods])
            return func

        return decorator

    def test_client(self):
        app = self

        class Client:
            def open(self, path, method='GET', json=None):
                func = app.routes[path][method]
                request.json = json
                resp = func()
                if not isinstance(resp, Response):
                    resp = Response(resp)
                return resp

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def get(self, path):
                return self.open(path, 'GET')

            def post(self, path, json=None):
                return self.open(path, 'POST', json=json)

        return Client()


# helpers

def jsonify(obj):
    return Response(json.dumps(obj))


def render_template(template_name, **context):
    import os

    template_path = os.path.join(os.path.dirname(__file__), '..', 'aerosketch', 'templates', template_name)
    with open(template_path, 'r') as f:
        template = f.read()
    rendered = template.format(**context)
    return Response(rendered)

# Global request proxy used inside handlers when running with test_client
request = Request()
