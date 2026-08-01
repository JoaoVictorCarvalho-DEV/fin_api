from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    response = exception_handler(
        exc,
        context
    )


    if isinstance(exc, Exception):

        status_code = getattr(
            exc,
            "status_code",
            None
        )

        if status_code:

            return Response(
                {
                    "detail": str(exc)
                },
                status=status_code
            )


    return response