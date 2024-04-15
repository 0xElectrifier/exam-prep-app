from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

from .exceptions import ApplicationError, InternalError


# logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    Inspiration for this was gotten from HackSoftware Django styleguide:
    https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file\
    #approach-2---hacksofts-proposed-way
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, context)

    # if unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
            }
            if exc.errors: # Only add the 'errors' field when it's not empty
                data.update({
                    'errors': {
                        'fields': exc.errors
                    }
                })
            return Response(data, status=400)
        elif isinstance(exc, InternalError):
            return Response(data={}, status=500)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }
    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation Failed"
        response.data["errors"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        # response.data["errors"] = {}

    del response.data["detail"]

    return response
