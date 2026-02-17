"""
Configuration file for Expense Tracker
Simple version without dotenv dependency
"""

import os

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')
    DEBUG = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    # Application settings
    PORT = int(os.environ.get('PORT', 5000))
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}