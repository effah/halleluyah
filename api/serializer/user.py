from rest_framework import serializers, viewsets
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
		instance.save()
		return instance

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer