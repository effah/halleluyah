from rest_framework import serializers
from api.models import Bible

class BibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bible
        fields = ('id', 'book', 'chapter','verses',)