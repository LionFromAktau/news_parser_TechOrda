from rest_framework import serializers
from . import models
from dateutil.parser import parse
class ItemCreateSerializer(serializers.Serializer):
    resource_name = serializers.CharField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Items
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['added_unix_date'] = int(parse(data['added_unix_date']).timestamp())
        return data

class ResourceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = models.Resource
        fields = '__all__'