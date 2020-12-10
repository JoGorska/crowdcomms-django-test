from datetime import datetime

from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        data = {
            'version': 1.0,
            'time': timezone.now(),
            'recent_visitors': 0,
            'all_visitors': 0,
            'all_visits': 0,
        }
        return Response(data)

