# Database Schema Definitions

SYMBOL_TABLE = '''
    CREATE TABLE IF NOT EXISTS symbol (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT UNIQUE NOT NULL
    )
'''

MONTHLY_PRICE_TABLE = '''
    CREATE TABLE IF NOT EXISTS monthly_price (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        FOREIGN KEY (symbol_id) REFERENCES symbol(id),
        UNIQUE(symbol_id, year, month)
    )
'''

# Create indexes for optimal query performance
CREATE_INDEX_SYMBOL_YEAR = 'CREATE INDEX IF NOT EXISTS idx_monthly_price_symbol_year ON monthly_price(symbol_id, year)'
CREATE_INDEX_SYMBOL = 'CREATE INDEX IF NOT EXISTS idx_monthly_price_symbol ON monthly_price(symbol_id)'
CREATE_UNIQUE_INDEX = 'CREATE UNIQUE INDEX IF NOT EXISTS idx_monthly_price_unique ON monthly_price(symbol_id, year, month)'

# All tables to create
TABLES = [
    SYMBOL_TABLE,
    MONTHLY_PRICE_TABLE,
]

# Index creation statements (executed after tables)
INDEXES = [
    CREATE_UNIQUE_INDEX,
    CREATE_INDEX_SYMBOL_YEAR,
    CREATE_INDEX_SYMBOL,
]

# Dummy data for initial setup
DUMMY_DATA = {
    'symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
}

