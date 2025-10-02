from typing import Final

APPLICATION_FORBIDDEN: Final[str] = "The user does not have access to this operation."

USER_ALREADY_EXISTS: Final[str] = "User already exists."

INVALID_LOGIN_OR_PASSWORD: Final[str] = "Invalid username or password."
INVALID_TOKEN: Final[str] = "Invalid token."
INVALID_CREDENTIALS: Final[str] = "Invalid credentials."

UNAUTHORIZED: Final[str] = "User is not authorized."
UNAUTHENTICATED: Final[str] = "The user failed authentication."
EXPIRED_SIGNATURE: Final[str] = "Your token has expired. Please log in again."
DECODE: Final[str] = "Your token has expired. Please log in again."
MISSION_REQUIRED_CLAIM: Final[str] = "There is no required field in your token."

USER_SESSION_NOT_FOUND: Final[str] = "The user session has not been found."
USER_ALREADY_AUTHENTICATED: Final[str] = "The user has already been authenticated."
