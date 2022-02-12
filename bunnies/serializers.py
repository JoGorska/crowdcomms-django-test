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

    def limit_bunnies_in_hole(self, obj):
        current_bunny_count = self.get_bunny_count()
        current_hole_in_request = self.request.rabbithole
        hole_id = current_hole_in_request.id
        current_hole = RabbitHole.objects.filter(id=hole_id)
        current_limit = current_hole.bunnies_limit
        if current_bunny_count > current_limit:
            raise serializers.ValidationError

    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner')


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        return []

    def validate(self, attrs):
        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')

