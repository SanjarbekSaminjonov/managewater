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


# class BasinViewSerializer(serializers.ModelSerializer):
#     messages = BasinMessageSerializer(many=True)
#
#     class Meta:
#         model = Basin
#         fields = '__all__'
#
#
# class BasinMessageViewSerializer(serializers.ModelSerializer):
#     basin = BasinSerializer(many=False)
#
#     class Meta:
#         model = BasinMessage
#         fields = '__all__'
