import sqlite3
from models.models import User, UserRole

DB_PATH = "urban_mobility.db"

def validate_credentials(username, password):
    return User(1, 'super_admin', 'Admin_123?', 'admin@gmail.com', UserRole.SUPER_ADMIN)