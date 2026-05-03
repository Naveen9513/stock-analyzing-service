# Stock Market Data REST API

A robust, layered REST API built with **FastAPI** to fetch, cache, and aggregate monthly stock market data using the Alpha Vantage external provider.

---

## Project Overview
This project provides a centralized service to analyze annual stock performance. It follows a clean architecture pattern to separate infrastructure, data access, and business logic, ensuring the code is maintainable and testable.

### Key Architecture Principles
*   **Layered Design:** Distinct separation between API Routers, Service Layer, and Repository Layer.
*   **Dependency Injection:** Services and Repositories are injected to promote loose coupling.
*   **Single Responsibility:** Database configuration, validation, and API communication each have dedicated classes.
*   **Data Persistence:** Local SQLite storage to minimize external API calls and improve latency.

---

## Technical Stack
*   **Framework:** FastAPI (Python 3.9+)
*   **Database:** SQLite (Raw SQL queries, no ORM)
*   **Validation:** Pydantic
*   **External API:** Alpha Vantage

---

## Installation & Setup

### 1. Environment Configuration
Create a `.env` file by duplicating the `.env.example` file in the root directory to store sensitive configuration:

```ini
# .env
ALPHA_VANTAGE_API_KEY=your_api_key_here
DATABASE_PATH=data/stocks.db
```

### 2. Install Dependencies
Install the required packages using the provided requirements file:

```bash
pip install -r requirements.txt
```

### 3. Database Initialization
The application is designed to automatically initialize the SQLite database and create necessary tables (symbol, monthly_price, symbol_fetched) and indexes upon the first startup.

## 4. Running the Application
Start the local development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```
The API will be available at http://localhost:8000. You can view the auto-generated documentation at http://localhost:8000/docs.

## API Endpoints
### GET /symbols/{symbol}/annual/{year}
Retrieves an annual summary for a specific stock ticker.

Parameters:

symbol (string): The stock ticker (e.g., AAPL). Validated for length and character type.

year (integer): The year of interest (e.g., 2023).

Success Response (200 OK):
```json
{
    "symbol": "AAPL",
    "year": 2025,
    "high": 260.5,
    "low": 225,
    "volume": 420000000
}
```
## Error Handling
The API utilizes a Global Exception Manager to catch custom application errors (e.g., DataNotFoundError, ExternalAPIError) and return standardized JSON responses.

404 Not Found: Returned when data is unavailable in both the local DB and the external API.

422 Unprocessable Entity: Returned when input parameters fail Pydantic validation.

503 Service Unavailable: Returned when the external data provider is unreachable.