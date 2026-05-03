from datetime import datetime

class SymbolRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_aggregated_data(self, symbol: str, year: int):
        """
        Get aggregated data for a specific year.
        """
        query = """
            SELECT MAX(mp.high), MIN(mp.low), SUM(mp.volume)
            FROM symbol s
            LEFT JOIN monthly_price mp ON s.id = mp.symbol_id AND mp.year = ?
            WHERE s.symbol = ?
            GROUP BY s.id
        """
        with self.db_manager.get_connection() as conn:
            cursor = conn.execute(query, (year, symbol.upper()))
            row = cursor.fetchone()

            if not row:
                return None

            high, low, volume = row
            return {
                "symbol": symbol.upper(),
                "year": year,
                "high": high,
                "low": low,
                "volume": volume
            }

    def get_aggregated_data_with_fetch_date(self, symbol: str, year: int):
        """
        Get aggregated data AND last fetch date in a single query.
        This combines two separate queries into one for better performance.

        Returns:
            tuple: (aggregated_data_dict, last_fetch_date) or (None, None) if no data
        """
        query = """
            SELECT MAX(mp.high), MIN(mp.low), SUM(mp.volume), sf.last_fetch_date
            FROM symbol s
            LEFT JOIN monthly_price mp ON s.id = mp.symbol_id AND mp.year = ?
            LEFT JOIN symbol_fetched sf ON s.id = sf.symbol_id
            WHERE s.symbol = ?
            GROUP BY s.id
        """
        with self.db_manager.get_connection() as conn:
            cursor = conn.execute(query, (year, symbol.upper()))
            row = cursor.fetchone()

            if not row:
                return None, None

            # Extract values
            high, low, volume, last_fetch_date_str = row

            # If no monthly data for this year
            if high is None:
                aggregated_data = None
            else:
                aggregated_data = {
                    "symbol": symbol.upper(),
                    "year": year,
                    "high": high,
                    "low": low,
                    "volume": volume
                }

            # Parse last_fetch_date if it exists
            last_fetch_date = None
            if last_fetch_date_str:
                try:
                    last_fetch_date = datetime.fromisoformat(last_fetch_date_str)
                except (ValueError, TypeError):
                    last_fetch_date = None

            return aggregated_data, last_fetch_date
    
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

            # 4. Update the symbol_fetched table to mark this symbol as fetched
            conn.execute(
                "INSERT OR REPLACE INTO symbol_fetched (symbol_id, last_fetch_date) VALUES (?, ?)",
                (symbol_id, datetime.now())
            )
            conn.commit()
    
