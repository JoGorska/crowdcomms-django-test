from django import get_version
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from bunnies.models import Bunny, RabbitHole


class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(many=True, queryset=Bunny.objects.all())
    bunny_count = serializers.SerializerMethodField()
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    
    def get_bunny_count(self, obj):
        return obj.bunnies.count()
    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner')


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        obj.family_members = []
        initial_data = self.get_initial()
        current_rabbithole_name = initial_data["home"]
        current_rabbit_name = initial_data["name"]
        rabbithole_object = get_object_or_404(RabbitHole, location=current_rabbithole_name)
        all_bunnies = Bunny.objects.filter(home=rabbithole_object).all()
        for bunny in all_bunnies:
            bunny_name = bunny.name
            obj.family_members.append(bunny_name)
        obj.family_members.remove(current_rabbit_name)
        return obj.family_members

    def validate(self, attrs):
        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')

