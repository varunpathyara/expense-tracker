"""
Configuration file for Expense Tracker Application
Loads environment variables and provides configuration settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # MySQL Database settings
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'expense_tracker')
    
    # Application settings
    PORT = int(os.getenv('PORT', 5000))
    
    # File upload settings (for future enhancements)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    @staticmethod
    def init_app(app):
        """Initialize application with this config"""
        pass

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    # In production, you should use environment variables
    
class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    MYSQL_DB = 'expense_tracker_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
