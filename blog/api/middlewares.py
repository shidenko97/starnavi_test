from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now


class SetLastActionMiddleware(MiddlewareMixin):
    """Middleware for setting last action time after each API requests"""

    def process_response(
            self,
            request: HttpRequest,
            response: HttpResponse
    ) -> HttpResponse:
        """
        Process each response from API
        :param request: Received request
        :type request: HttpRequest
        :param response: API view response
        :type response: HttpResponse
        :return: API view response
        :rtype: HttpResponse
        """

        # If user is authenticated - set his/her last_action datetime
        if request.user.is_authenticated:
            get_user_model().objects.filter(pk=request.user.pk).update(
                last_action=now()
            )

        return response
