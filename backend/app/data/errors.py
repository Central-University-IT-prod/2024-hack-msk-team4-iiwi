from fastapi import HTTPException, status


class Errors(Exception):
    """
    This module defines custom error responses for the application using the `HTTPException` class from FastAPI.

    Classes:
        Errors (Enum): An enumeration of custom HTTP exceptions used throughout the application.

        Attributes:
            CREDENTIALS_EXCEPTION (HTTPException): Raised when the provided credentials are invalid.
            INACTIVE_USER_EXCEPTION (HTTPException): Raised when the user account is inactive.
            USER_NOT_FOUND_EXCEPTION (HTTPException): Raised when the specified user is not found in the system.
            PERMISSION_DENIED_EXCEPTION (HTTPException): Raised when the user does not have the necessary permissions to access a resource.
            SERVER_ERROR_EXCEPTION (HTTPException): Raised when an unexpected server error occurs.
            UNAUTHORIZED_EXCEPTION (HTTPException): Raised when the username or password is incorrect.
    """

    EVENT_NOT_FOUND_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found.",
    )

    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please ensure that your username and password are correct and try again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    """
    Raised when the specified user is not found in the system.
    """

    PERMISSION_DENIED_EXCEPTION = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied. You do not have the necessary permissions to access this resource.",
    )
    """
    Raised when the user does not have the necessary permissions to access a resource.
    """

    SERVER_ERROR_EXCEPTION = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail="Internal server error. An unexpected error occurred on the server. Please try again later.",
    )
    
    CATEGORY_NOT_FOUND_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found.",
    )
    
    """
    Raised when the user account is inactive.
    """
    UNAUTHORIZED_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please ensure that your username and password are correct and try again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    """
    Raised when the provided credentials are invalid.
    """

    USER_NOT_FOUND_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found. The user you are trying to access does not exist in our system.",
    )
    
    
    CODE_INVALID = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Out sms code is invalid "
    )
    
    DEBTER_NOT_FOUND_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Debter not found"
    )