#!/usr/bin/env python3
""" This module contains the Auth class """
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        return False
    
    def authorization_header(self, request=None) -> str:
        return None
    
    def current_user(self, request=None):
        return None
