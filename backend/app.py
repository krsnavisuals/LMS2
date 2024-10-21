import os
from flask import Flask
from flask_cors import CORS
from db import init_db
from flask_jwt_extended import JWTManager
from cache import cache
import redis
from dotenv import load_dotenv
from datetime import timedelta

from ebooks import ebooks_bp
from sections import sections_bp
from users import users_bp
from ebook_requests import ebook_requests_bp
from feedback import feedback_bp
from stats import stats_bp

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure cache with environment variables
app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_HOST"] = os.getenv("CACHE_REDIS_HOST")
app.config["CACHE_REDIS_PORT"] = int(os.getenv("CACHE_REDIS_PORT") or "")
app.config["CACHE_REDIS_PASSWORD"] = os.getenv("CACHE_REDIS_PASSWORD")
app.config["CACHE_REDIS_DB"] = int(os.getenv("CACHE_REDIS_DB") or 0)
app.config["CACHE_DEFAULT_TIMEOUT"] = int(os.getenv("CACHE_DEFAULT_TIMEOUT") or 300)

# Initialize cache
cache.init_app(app)
redis_client = redis.Redis(
    host=os.getenv("CACHE_REDIS_HOST") or "localhost",
    port=int(os.getenv("CACHE_REDIS_PORT") or "123123"),
    password=os.getenv("CACHE_REDIS_PASSWORD")
)

CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWTT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Register the blueprints
app.register_blueprint(ebooks_bp)
app.register_blueprint(sections_bp)
app.register_blueprint(users_bp)
app.register_blueprint(ebook_requests_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(stats_bp)

init_db()

@app.route("/", methods=["GET"])
def is_api_up():
    return "API is running."

if __name__ == "__main__":
    app.run(debug=True)
