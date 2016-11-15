from rest_framework import serializers
from api.models import Photo

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'photo', 'thumbnail',)