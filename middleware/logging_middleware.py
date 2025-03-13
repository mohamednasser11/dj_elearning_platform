# middleware/logging_middleware.py
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to execute before the view is called
        self.log_request(request)

        # Call the next middleware or the view
        response = self.get_response(request)

        # Code to execute after the view is called
        self.log_response(request, response)

        return response

    def log_request(self, request):
        """Log details of the incoming request."""
        logger.info(
            f"Incoming Request: {request.method} {request.path} - User: {request.user}"
        )

    def log_response(self, request, response):
        """Log details of the outgoing response."""
        logger.info(
            f"Outgoing Response: {request.method} {request.path} - Status: {response.status_code}"
        )