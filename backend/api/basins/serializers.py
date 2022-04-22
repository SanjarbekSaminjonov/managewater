from rest_framework import serializers
from basins.models import Basin, BasinMessage


class BasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basin
        fields = '__all__'


class BasinMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasinMessage
        fields = '__all__'
