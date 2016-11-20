from rest_framework import serializers
from api.models import Post 
from api.serializer.user import UserViewSerializer
from api.serializer.gallery import GallerySerializer
from api.serializer.bible import BibleSerializer
from api.serializer.like import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'message', 'gallery', 'quotation', 'likes','comments','created','updated')
    
    def create(self,validated_data):  
        user_post = Post.objects.create(user=validated_data['user'],message=validated_data['message'])   
        return user_post
    
    def update(self,instance,validated_data):
        return

class PostViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserViewSerializer(many=False)
    message = serializers.CharField()
    gallery = GallerySerializer(many=True)
    quotation = BibleSerializer(many=True)
    likes = LikeSerializer(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()