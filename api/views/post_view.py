from rest_framework import status 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from api.serializer.post import PostSerializer, PostViewSerializer
from api.models import User, Like, Photo, Bible, Post
import logging

class PostList(generics.ListAPIView):
    model = Post
    serializer_class = PostViewSerializer

    def get_queryset(self):   
        return Post.objects.all()

    def post(self,request,api_version,format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            my_post = Post.objects.get(id=serializer.data['id']) 
            if 'photos' in request.data:
                for photo in request.data.getlist('photos'):
                    my_post.gallery.add(Photo.objects.create(user=my_post.user, photo=photo))  
            
            if 'bibles' in request.data:
                logging.error("Has Bible.")
            
            serializer = PostViewSerializer(my_post)        
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    model = Post
    serializer_class = PostViewSerializer
    
    def get_object(self,pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Http404

    def get(self,request,api_version,pk,format=None):
        post = self.get_object(pk)
        serializer = PostViewSerializer(post)
        return Response(serializer.data)

    def put(self,request,api_version,pk,format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
            
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,api_version,pk,format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)