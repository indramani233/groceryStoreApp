# config.py
# config.py

# Add configurations for caching (modify as needed)
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = ''
CACHE_REDIS_PASSWORD = ''
CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds (adjust as needed)

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = 'your_secret_key'
    # Add other configurations as needed
    EXPORT_PATH='D:\\Sanchay\\Desktop\\iit madras\\appdev2\\GS\\'
