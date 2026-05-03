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