import os

class Config:
     # Secret key untuk security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Konfigurasi database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Konfigurasi tambahan
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file upload 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
