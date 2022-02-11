from datetime import datetime
from django.shortcuts import get_object_or_404

from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import UserVisit


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):

        
        user_from_request = request.user
        user_id = user_from_request.id
        user_object = get_object_or_404(User, id=user_id)
        all_visits_objects = UserVisit.objects.all()
        users_already_in = []
        # checks if user already has UserVisit
        for visit in all_visits_objects:
            users_already_in.append(visit.user)
        if user_object in users_already_in:
            # updates the UserVisit object if user already has an object
            user_visit_object = get_object_or_404(UserVisit, user=user_object)
            current_visits = user_visit_object.visits 
            new_visits = current_visits + 1
            user_visit_object.visits = new_visits
            user_visit_object.last_seen = datetime.now()
            user_visit_object.save(
                update_fields=["last_seen", "visits",]
            )
            
        else:
            # creates new UserVisit object if user doesn't have this object yet
            user_visit = UserVisit.objects.create(
                user = user_object,

            )
        # for loop to get summary of all visits from each user
        all_visits = 0
        for visit in all_visits_objects:
            all_visits += visit.visits
        
        data = {
            'version': 1.0,
            'time': datetime.now(),
            'recent_visitors': UserVisit.objects.count(),
            'all_visitors': User.objects.count(),
            'all_visits': all_visits,
        }
        return Response(data)
    
            

    

        



