from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from django.core.exceptions import ValidationError

logger = logging.getLogger("django")


def custom_exception_handler(exc, context):
    """
    The function `custom_exception_handler` handles custom exceptions by mapping them to specific
    handlers and returning a response with the appropriate status code and message.

    :param exc: The `exc` parameter is the exception object that was raised. It contains information
    about the exception, such as its type, message, and traceback
    :param context: The `context` parameter in the `custom_exception_handler` function is a dictionary
    that contains information about the current request and view that raised the exception. It typically
    includes the following keys:
    :return: a response object.
    """
    try:
        exception_class = exc.__class__.__name__
        handlers = {
            "NotAuthenticated": _handler_authentication_error,
            "InvalidToken": _handler_invalid_token_error,
            "ValidationError": _handler_validation_error,
            "ParseError": _handler_parse_error,  # Nouveau handler pour les erreurs de parsing
            "UnsupportedMediaType": _handler_unsupported_media_type_error,  # Nouveau handler pour les fichiers non supportés
            # Ajoute d'autres handlers ici
        }
        res = exception_handler(exc, context)
        if exception_class in handlers:
            message = handlers[exception_class](exc, context, res)
        else:
            message = str(exc)

        return Response(data={}, status=res.status_code, message=message)
    except Exception as e:
        logger.error(str(e))
        return Response({"message": "An internal error occurred"}, status=500)


def _handler_authentication_error(exc, context, response):
    """
    The function returns a message indicating that an authorization token is not provided.

    :param exc: The `exc` parameter is the exception object that was raised during the authentication
    process
    :param context: The `context` parameter is a dictionary that contains additional information about
    the error that occurred. It can include details such as the request that caused the error, the user
    who made the request, or any other relevant information
    :param response: The `response` parameter is the HTTP response object that will be returned to the
    client. It contains information such as the status code, headers, and body of the response
    :return: the string "An authorization token is not provided."
    """
    return "An authorization token is not provided."


def _handler_invalid_token_error(exc, context, response):
    """
    The function handles an invalid token error by returning a specific error message.

    :param exc: The `exc` parameter represents the exception that was raised. In this case, it would be
    an invalid token error
    :param context: The `context` parameter is a dictionary that contains additional information about
    the error that occurred. It can include details such as the request that caused the error, the user
    who made the request, or any other relevant information
    :param response: The `response` parameter is the HTTP response object that will be returned to the
    client. It contains information such as the status code, headers, and body of the response
    :return: the string "An authorization token is not valid."
    """
    return "An authorization token is not valid."


def _handler_parse_error(exc, context, response):
    """
    Handle ParseError (e.g., missing required fields during upload).
    """
    return "Required field is missing or malformed."


def _handler_unsupported_media_type_error(exc, context, response):
    """
    Handle UnsupportedMediaType (e.g., invalid file extension).
    """
    return "The file type is not supported."


def _handler_validation_error(exc, context, response):
    """
    Handle ValidationError with custom messages.
    """
    key = list(list(exc.__dict__.values())[0].keys())[0]
    try:
        code = list(list(exc.__dict__.values())[0].values())[0][0].__dict__["code"]
        value = list(list(exc.__dict__.values())[0].values())[0][0]
    except:
        code = list(list(exc.__dict__.values())[0].values())[0][0][0].__dict__["code"]
        value = list(list(exc.__dict__.values())[0].values())[0][0][0]

    custom_msg_code = ["required", "null", "blank"]
    if code in custom_msg_code:
        message = f"{key} field is required"
    else:
        message = str(value)

    return message
