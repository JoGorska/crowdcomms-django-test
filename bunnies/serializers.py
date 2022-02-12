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

    def pass_limit_bunnies_in_hole(self, obj):
        looking_for_limit = obj.__dict__["bunnies_limit"].__dict__
        print(f'RABBIT HOLE LIMIT {looking_for_limit}')

    # current_bunny_count = self.get_bunny_count(self, obj)
    #     # current_limit = obj.rabbithole.bunnies_limit
    #     current_limit = 2
    #     if current_bunny_count <= current_limit:
    #         return True

        initial_data = self.__dict__["_declared_fields"]["bunnies"].__dict__["_kwargs"]["child_relation"].queryset
        current_bunny_count = 0
        for bunny in initial_data:
            current_bunny_count += 1
        return current_bunny_count

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
        if not RabbitHoleSerializer.pass_limit_bunnies_in_hole(RabbitHoleSerializer, RabbitHole):
            return self.context
        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')

