from rest_framework import serializers

from .models import BotResponse


class BotResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotResponse
        fields = "__all__"
