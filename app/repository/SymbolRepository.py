class SymbolRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_aggregated_data(self, symbol: str, year: int):
        query = """
            SELECT MAX(mp.high), MIN(mp.low), SUM(mp.volume)
            FROM monthly_price mp
            JOIN symbol s ON mp.symbol_id = s.id
            WHERE s.symbol = ? AND mp.year = ?
        """
        with self.db_manager.get_connection() as conn:
            cursor = conn.execute(query, (symbol.upper(), year))
            row = cursor.fetchone()
            
            if row and row[0] is not None:
                return {
                    "symbol": symbol.upper(),
                    "year": year,
                    "high": row[0],
                    "low": row[1],
                    "volume": row[2]
                }
            return None
    
    def save_monthly_data(self, symbol: str, incoming_data: dict):
        """
        Processes and saves the dict format:
        {'data': {'2025-01': {...}, ...}}
        """
        monthly_dict = incoming_data['data']

        with self.db_manager.get_connection() as conn:
            # 1. Ensure symbol exists and get its ID
            cursor = conn.execute(
                "INSERT OR IGNORE INTO symbol (symbol) VALUES (?)", (symbol,)
            )
            # Fetch the ID (whether we just inserted it or it already existed)
            cursor = conn.execute("SELECT id FROM symbol WHERE symbol = ?", (symbol,))
            symbol_id = cursor.fetchone()[0]

            # 2. Prepare the batch data
            # We split the 'YYYY-MM' key to get year and month separately
            insert_payload = []
            for date_str, metrics in monthly_dict.items():
                year_val, month_val = map(int, date_str.split('-'))
                insert_payload.append((
                    symbol_id, 
                    year_val, 
                    month_val, 
                    metrics['open'], 
                    metrics['high'], 
                    metrics['low'], 
                    metrics['close'], 
                    metrics['volume']
                ))

            # 3. Batch insert/replace using the UNIQUE constraint (symbol_id, year, month)
            query = """
                INSERT OR REPLACE INTO monthly_price 
                (symbol_id, year, month, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            conn.executemany(query, insert_payload)
            conn.commit()
    
