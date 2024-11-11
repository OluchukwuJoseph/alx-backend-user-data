#!/usr/bin/env python3
""" This script functions for hashing user password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Generate salted, hashed password """
    byte: bytes = password.encode()
    salt: bytes = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(byte, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Checks if the plain text password matches the hashed password """
    return bcrypt.checkpw(password.encode(), hashed_password)
