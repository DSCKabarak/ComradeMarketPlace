from rest_framework import status
from rest_framework.response import Response


class ApiResponse:
    @staticmethod
    def success(message=None, data=None):
        return Response(
            {"success": True, "message": message, "data": data},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def created(message=None, data=None):
        return Response(
            {"success": True, "message": message, "data": data},
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def bad_request(message=None, errors=None):
        return Response(
            {"success": False, "message": message or "Bad request", "errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def unauthorized(message=None):
        return Response(
            {"success": False, "message": message or "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def forbidden(message=None):
        return Response(
            {"success": False, "message": message or "Forbidden"},
            status=status.HTTP_403_FORBIDDEN,
        )

    @staticmethod
    def not_found(message=None):
        return Response(
            {"success": False, "message": message or "Not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def method_not_allowed(message=None):
        return Response(
            {"success": False, "message": message or "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @staticmethod
    def no_content(message=None):
        return Response(
            {"success": False, "message": message or "No content"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @staticmethod
    def server_error(message=None):
        return Response(
            {"success": False, "message": message or "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
