import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "not so secret key")
    MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10 MB


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
