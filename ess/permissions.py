"""
permissions.py

@Author:    Maro Okegbero
@Date:      Oct 28, 2023


This module contains all the bespoke permissions for the project
"""


from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow administrators
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        return request.user.is_administrator

