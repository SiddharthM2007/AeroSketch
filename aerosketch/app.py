from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .routes.simulate import bp as simulate_bp
    from .routes.parameters import bp as parameters_bp
    from .routes.results import bp as results_bp
    from .routes.optimization import bp as optimization_bp
    from .routes.dashboard import bp as dashboard_bp

    app.register_blueprint(simulate_bp)
    app.register_blueprint(parameters_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(optimization_bp)
    app.register_blueprint(dashboard_bp)

    return app
