# middleware/logging_middleware.py
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request(request)

        response = self.get_response(request)

        self.log_response(request, response)

        return response

    def log_request(self, request):
        logger.info(
            f"Incoming Request: {request.method} {request.path} - User: {request.user}"
        )

    def log_response(self, request, response):
        logger.info(
            f"Outgoing Response: {request.method} {request.path} - Status: {response.status_code}"
        )