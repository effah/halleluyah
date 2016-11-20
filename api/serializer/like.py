from rest_framework import serializers
from api.models import Like
from api.serializer.user import UserViewSerializer

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'vote')
    
    def create(self, validated_data): 
        return Like.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.vote = validated_data.get('vote', instance.vote)
        instance.save()
        return instance

class LikeViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserViewSerializer(many=False)
    vote = serializers.IntegerField()
