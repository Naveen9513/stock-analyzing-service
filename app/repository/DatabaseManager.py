import sqlite3
import os
from app.database.schema import TABLES, INDEXES

# Get absolute path from environment variable
db_path_env = os.getenv('DATABASE_PATH')
db_name_env = os.getenv('DATABASE_NAME', 'stock.db')

if db_path_env:
    # If absolute path is provided, use it directly
    if os.path.isabs(db_path_env):
        DB_PATH = os.path.join(db_path_env, db_name_env)
    else:
        # If relative, resolve from project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        DB_PATH = os.path.join(project_root, db_path_env, db_name_env)
else:
    # Default fallback
    DB_PATH = os.path.join(os.path.dirname(__file__), db_name_env)

class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = self._get_default_db_path()
        self.db_path = db_path
    
    def get_connection(self):
        """Get a connection to the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize the database with required tables and indexes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create all tables from schema
        for table_schema in TABLES:
            cursor.execute(table_schema)
        
        # Create indexes
        for index_schema in INDEXES:
            cursor.execute(index_schema)
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
    def _get_default_db_path(self):
        """Calculate database path from environment variables"""
        db_path_env = os.getenv('DATABASE_PATH')
        db_name_env = os.getenv('DATABASE_NAME', 'stock.db')
        
        if db_path_env:
            if os.path.isabs(db_path_env):
                return os.path.join(db_path_env, db_name_env)
            else:
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                return os.path.join(project_root, db_path_env, db_name_env)
        else:
            return os.path.join(os.path.dirname(__file__), db_name_env)

