from pydantic import BaseModel, Field, field_validator

class SymbolStatRequestValidator(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    year: int = Field(..., description="The year of the data to fetch")

    # Custom validation logic for the symbol
    @field_validator('symbol')
    def validate_symbol(cls, value):
        if not value.isalpha():
            raise ValueError('Symbol must contain only letters (e.g., AAPL)')
        return value.upper()

    # Custom validation logic for the year
    @field_validator('year')
    def validate_year(cls, value):
        if value < 1900 or value > 2100:
            raise ValueError('Year must be between 1900 and 2100')
        return value