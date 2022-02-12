from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from bunnies.models import Bunny, RabbitHole
from bunnies.permissions import RabbitHolePermissions
from bunnies.serializers import BunnySerializer, RabbitHoleSerializer


class RabbitHoleViewSet(viewsets.ModelViewSet):
    serializer_class = RabbitHoleSerializer
    permission_classes = (IsAuthenticated, RabbitHolePermissions)
    queryset = RabbitHole.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, *args, **kwargs):
        current_user = self.request.user
        user_id = current_user.id
        user_object = User.objects.get(id=user_id)
        owns_holes = RabbitHole.objects.filter(owner=user_object).all()

        return owns_holes



class BunnyViewSet(viewsets.ModelViewSet):
    serializer_class = BunnySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bunny.objects.all()