from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.exception.Exceptions import DataNotFoundError, ExternalAPIError, ValidationError

class ExceptionManager:
    @staticmethod
    def register_handlers(app: FastAPI):
        
        @app.exception_handler(DataNotFoundError)
        async def handle_not_found(request: Request, exc: DataNotFoundError):
            return JSONResponse(
                status_code=404,
                content={"error": "Data Not Found", "message": str(exc)}
            )

        @app.exception_handler(ExternalAPIError)
        async def handle_api_error(request: Request, exc: ExternalAPIError):
            return JSONResponse(
                status_code=503,
                content={"error": "External Service Unavailable", "message": str(exc)}
            )
        
        @app.exception_handler(ValidationError)
        async def handle_validation_error(request: Request, exc: ValidationError):
            return JSONResponse(
                status_code=422,
                content={"error": "Validation Error", "message": str(exc)}
            )

        @app.exception_handler(Exception)
        async def handle_global_error(request: Request, exc: Exception):
            print(exc)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": "Something went wrong"}
            )