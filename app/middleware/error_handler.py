from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger_config import setup_logger

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for exception handling and logging."""
    def __init__(self, app):
        super().__init__(app)
        # Initialize logger for error handling
        self.logger = setup_logger("error_handler")

    async def dispatch(self, request: Request, call_next):
        try:
            # Process request and pass to next middleware
            response = await call_next(request)
            return response
        except HTTPException as e:
            # Log HTTP-specific exceptions
            self.logger.error(f"HTTP Exception: {e.status_code} - {e.detail}")
            # Return JSON response with error details
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            # Log unexpected exceptions with stack trace
            self.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            # Return generic server error response
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )

def add_error_handler_middleware(app):
    """Register error handler middleware with the application."""
    app.add_middleware(ErrorHandlerMiddleware)