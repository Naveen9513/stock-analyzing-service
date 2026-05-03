# Database Schema Definitions

SYMBOL_TABLE = '''
    CREATE TABLE IF NOT EXISTS symbol (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT UNIQUE NOT NULL
    )
'''

# Add more tables here as needed in the future
TABLES = [
    SYMBOL_TABLE,
]

# Dummy data for initial setup
DUMMY_DATA = {
    'symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
}
