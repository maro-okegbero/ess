"""
utils.py

@Author:    Maro Okegbero
@Date:      OCT 28, 2023

This module contains a number of utility functions
No references are made to specific models or views. As a result, they are useful with or
without the application context.
"""
import uuid



def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None
