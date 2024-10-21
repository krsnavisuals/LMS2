from flask import Flask
from flask_caching import Cache
from ebooks import ebooks_bp

def create_app():
    app = Flask(__name__)

    # Configure Redis cache
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    cache = Cache(app)

    # Register blueprint
    app.register_blueprint(ebooks_bp)

    return app, cache
