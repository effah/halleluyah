from rest_framework import status 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from api.serializer.user import UserSerializer
from api.models import User 

class UserList(generics.ListAPIView):
	model = User
	serializer_class = UserSerializer

	def get_queryset(self):  
		return User.objects.all() 

	def post(self,request,api_version,format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
	model = User
	serializer_class = UserSerializer
	
	def get_object(self,token):
		try:
			return User.objects.get(id=token)
		except User.DoesNotExist:
			raise Http404

	def get(self,request,api_version,token,format=None):
		user = self.get_object(token)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	def put(self,request,api_version,token,format=None):
		user = self.get_object(token)
		serializer = UserSerializer(user, data=request.data)
			
		if(serializer.is_valid()):
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,api_version,token,format=None):
		user = self.get_object(token)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)