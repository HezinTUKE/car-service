from fastapi import HTTPException, status


class ServerException(HTTPException):
    def __init__(
        self,
        detail: str = "Internal server error",
        error_code: str = "SERVER_ERROR"
    ):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "error_code": error_code,
            "message": detail
        })


class BadRequestException(HTTPException):
    def __init__(
        self,
        detail: str = "Bad request",
        error_code: str = "BAD_REQUEST"
    ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "error_code": error_code,
            "message": detail
        })


class NotFoundException(HTTPException):
    def __init__(
        self,
        detail: str = "Resource not found",
        error_code: str = "NOT_FOUND"
    ):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error_code": error_code,
            "message": detail
        })


class DBException(HTTPException):
    def __init__(
        self,
        detail: str = "Database error",
        error_code: str = "DB_ERROR"
    ):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "error_code": error_code,
            "message": detail
        })


class TokenGenerationException(HTTPException):
    def __init__(
        self,
        detail: str = "Token generation error",
        error_code: str = "TOKEN_GEN_ERROR"
    ):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "error_code": error_code,
            "message": detail
        })


class InvalidCredentialsException(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid credentials",
        error_code: str = "INVALID_CREDENTIALS"
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            "error_code": error_code,
            "message": detail
        })


class IncorrectDataException(HTTPException):
    def __init__(
        self,
        detail: str = "Incorrect data provided",
        error_code: str = "INCORRECT_DATA"
    ):
        super().__init__(status_code=status.HTTP_401_BAD_REQUEST, detail={
            "error_code": error_code,
            "message": detail
        })


class ForbiddenException(HTTPException):
    def __init__(
        self,
        detail: str = "Forbidden",
        error_code: str = "FORBIDDEN"
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail={
            "error_code": error_code,
            "message": detail
        })


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        detail: str = "Unauthorized",
        error_code: str = "UNAUTHORIZED"
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            "error_code": error_code,
            "message": detail
        })
