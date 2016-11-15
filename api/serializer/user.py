from rest_framework import serializers
from api.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'fname', 'lname', 'phone', 'email', 'thumbnail','cover_photo','created','updated') 

	def create(self,validated_data): 
		return User.objects.create(**validated_data)

	def update(self,instance,validated_data):
		instance.fname = validated_data.get('fname',instance.fname)
		instance.lname = validated_data.get('lname',instance.lname)
		instance.phone = validated_data.get('phone',instance.phone)
		instance.email = validated_data.get('email',instance.email)
		instance.thumbnail = validated_data.get('thumbnail',instance.thumbnail)
		instance.cover_photo = validated_data.get('cover_photo',instance.cover_photo)
		instance.clean_image()
		instance.save()
		return instance

class UserViewSerializer(serializers.Serializer):
	id = serializers.UUIDField()
	fname = serializers.CharField()
	lname = serializers.CharField()
	thumbnail = serializers.FileField()