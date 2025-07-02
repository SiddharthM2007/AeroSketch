import json
from types import SimpleNamespace

class _Request(SimpleNamespace):
    def get_json(self):
        return self.json

request = _Request(json=None)

class Response:
    def __init__(self, data=b"", status=200, mimetype="application/json"):
        self.data = data
        self.status_code = status
        self.mimetype = mimetype
        self.content_type = mimetype

    def get_json(self):
        if self.mimetype == "application/json":
            return json.loads(self.data.decode())
        return None

class Flask:
    def __init__(self, name):
        self.name = name
        self.routes = {}
        self.config = {}

    def route(self, rule, methods=None):
        methods = methods or ["GET"]

        def decorator(func):
            self.routes[(rule, tuple(sorted(methods)))] = func
            return func

        return decorator

    def register_blueprint(self, bp):
        for (rule, methods), func in bp.routes.items():
            self.routes[(rule, methods)] = func

    def test_client(self):
        app = self

        class Client:
            def open(self, path, method="GET", json_data=None):
                key = (path, (method,))
                func = app.routes.get(key)
                request.json = json_data
                resp = func()
                if isinstance(resp, Response):
                    return resp
                elif isinstance(resp, tuple):
                    data, status = resp
                    if isinstance(data, Response):
                        data.status_code = status
                        return data
                return Response(json.dumps(resp).encode())

            def get(self, path):
                return self.open(path, method="GET")

            def post(self, path, json=None):
                return self.open(path, method="POST", json_data=json)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        return Client()


class Blueprint:
    def __init__(self, name, import_name):
        self.name = name
        self.routes = {}

    def route(self, rule, methods=None):
        methods = methods or ["GET"]

        def decorator(func):
            self.routes[(rule, tuple(sorted(methods)))] = func
            return func

        return decorator


def jsonify(obj):
    return Response(json.dumps(obj).encode())


def render_template(template_name, **context):
    with open(f"aerosketch/templates/{template_name}") as f:
        content = f.read()
    for k, v in context.items():
        if isinstance(v, dict):
            for subk, subv in v.items():
                content = content.replace(f"{{{{ {k}.{subk} }}}}", str(subv))
        else:
            content = content.replace(f"{{{{ {k} }}}}", str(v))
    return Response(content.encode(), mimetype="text/html")


def send_file(file, mimetype="application/octet-stream"):
    data = file.read()
    return Response(data, mimetype=mimetype)

__all__ = [
    "Flask",
    "Blueprint",
    "request",
    "jsonify",
    "render_template",
    "send_file",
    "Response",
]
