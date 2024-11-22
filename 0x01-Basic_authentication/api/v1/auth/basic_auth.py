#!/usr/bin/env python3
""" This module contains the BasicAuth class """
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class that extends the Auth class
    to implement Basic Authentication.

    This class provides methods to handle HTTP Basic Authentication by:
    1. Extracting the Base64 encoded credentials from the Authorization header
    2. Decoding the Base64 authorization header to retrieve credentials

    Inherits from Auth class to maintain authentication framework consistency.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string
                Expected format: "Basic <base64_credentials>"

        Returns:
            str: The Base64 encoded credentials part of the header or None
        """
        if authorization_header is None or \
            type(authorization_header) is not str or\
                not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decodes Base64-encoded authorization header
        to retrieve original credentials.

        Args:
            base64_authorization_header (str): The Base64 encoded authorization
                credentials string
                Expected format: "<base64_credentials>"

        Returns:
            str: The decoded string
                (typically in the format "username:password") or None
        """
        if base64_authorization_header is None or\
                type(base64_authorization_header) is not str:
            return None

        try:
            header_byte = base64_authorization_header.encode('utf-8')
            header_str = base64.b64decode(header_byte).decode('utf-8')
        except binascii.Error:
            return None

        return header_str

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user credentials (username and password) from a decoded Base64
        authorization header.

        Args:
        decoded_base64_authorization_header (str): The decoded authorization
            header Expected format: "username:password"

        Returns:
            Tuple[str, str]: A tuple containing (username, password) or None
        """
        if decoded_base64_authorization_header is None or\
                type(decoded_base64_authorization_header) is not str or\
                ':' not in decoded_base64_authorization_header:
            return (None, None)

        colon_idx = decoded_base64_authorization_header.find(':')
        return (decoded_base64_authorization_header[0:colon_idx],
                decoded_base64_authorization_header[colon_idx + 1:])

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a User instance based on email and password credentials.

        This method validates the email and password combination by:
        1. Checking if both email and password are valid strings
        2. Searching for a user with the provided email
        3. Validating the password matches the found user

        Args:
            user_email (str): The email address of the user
                trying to authenticate
            user_pwd (str): The password to validate against
                the user's stored password

        Returns:
            TypeVar('User'): A User instance if authentication succeeds or None
        """
        if user_email is None or type(user_email) is not str or\
                user_pwd is None or type(user_pwd) is not str:
            return None

        result = User.search({'email': user_email})
        if len(result) == 0:
            return None

        user = result[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request using Basic authentication.

        This method implements the complete Basic authentication flow:
        1. Extracts the Authorization header from the request
        2. Decodes the Base64 credentials
        3. Separates email and password
        4. Validates credentials and returns corresponding User

        Args:
            request: The HTTP request object containing the authorization
                header. Defaults to None

        Returns:
            TypeVar('User'): A User instance if authentication succeeds or None
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        decoded_authorization_header = self.decode_base64_authorization_header(
            base64_authorization_header)
        user_credentials = self.extract_user_credentials(
            decoded_authorization_header)
        user = self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])

        return user
