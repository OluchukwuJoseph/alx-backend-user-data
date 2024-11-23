#!/usr/bin/env python3
""" This module contains the Auth class """
from flask import request
from typing import List, TypeVar
import werkzeug


class Auth:
    """
    Authentication utility class that provides methods for handling
    authentication-related operations in a web application.

    This class implements methods for path-based authentication requirements,
    authorization header validation, and user context management.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication by checking against
        a list of excluded paths.

        Args:
            path (str): The URL path to check for authentication requirement.
                       Example: '/api/v1/users'
            excluded_paths (List[str]): List of paths that don't require
                                      authentication.
                                      Example: ['/api/v1/status/',
                                               '/api/v1/unauthorized/']

        Returns:
            bool: True if authentication is required, False if the path is in
                 excluded_paths.

        Note:
            This method normalizes both the input path and excluded paths by
            ensuring they end with a forward slash '/'.
            Example:
                path = '/api/v1/users' becomes '/api/v1/users/'
                excluded_paths = ['/api/v1/status'] becomes ['/api/v1/status/']
        """
        import re
        if excluded_paths is None or len(excluded_paths) == 0 or\
                path is None or len(path) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                path_pattern = rf"{excluded_path[:-1]}.*"
            else:
                if not path.endswith('/'):
                    path += '/'
                if not excluded_path.endswith('/'):
                    excluded_path += '/'
                path_pattern = rf"{excluded_path}"
            if re.match(path_pattern, path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves and validates the authorization header
        from the request object.

        Args:
            request (Optional[Request]): Flask request object containing HTTP
                                       request information.

        Returns:
            Optional[str]: The authorization header if present and valid,
                          None otherwise.

        Note:
            This method is typically used to extract authentication tokens or
            credentials from the request headers for further processing.
        """
        if request is not None:
            return request.headers.get('Authorization', None)

        return None

    def current_user(self, request=None):
        """
        Retrieves the current authenticated user based on the request context.

        Args:
            request (Optional[Request]): Flask request object containing HTTP
                                       request information.

        Returns:
            Optional[object]: None by default. This method is meant to be
                            overridden by child classes to implement specific
                            user retrieval logic.

        Note:
            This is a placeholder method that should be overridden by
            implementations to provide actual user retrieval functionality
            based on the application's authentication mechanism.
        """
        return None
