from rest_framework import status 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from api.serializer.post import PostSerializer, PostViewSerializer
from api.serializer.like import LikeViewSerializer, LikeSerializer
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
                    try:
                        my_post.gallery.add(Photo.objects.create(user=my_post.user, photo=photo)) 
                    except Exception:
                        pass 
            
            if 'bibles' in request.data:
                for bible in request.data.get('bibles'):
                    try:
                        my_post.quotation.add(
                            Bible.objects.create(
                                user=my_post.user, book=bible['book'],
                                chapter = bible['chapter'],verses = bible['verses']
                            )
                        )
                    except Exception:
                        pass 
            
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
            raise Http404

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

class LikeList(generics.ListAPIView):
    model = Like
    serializer_class = LikeViewSerializer
    
    def get_object(self,pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get_queryset(self,format='json'):
        post = self.get_object(self.kwargs['pk'])
        return post.likes.all()
    
    def post(self,request,api_version,pk,format=None):
        my_post = self.get_object(pk) 
        request.data['user'] = my_post.user.id
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():  
            my_post.likes.add(Like.objects.create(user=my_post.user, vote = serializer.data['vote']))
            serializer = LikeViewSerializer(my_post.likes, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeDetail(APIView):
    model = Like
    serializer_class = LikeViewSerializer
    
    def get_object(self,pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get_object_like(self,pk,lk):
        try:
            return self.get_object(pk).likes.get(id=lk)
        except Like.DoesNotExist:
            raise Http404
    
    def get(self,request,api_version,pk,lk,format=None):
        like = self.get_object_like(pk,lk)
        serializer = LikeViewSerializer(like) 
        return Response(serializer.data)
    
    def delete(self,request,api_version,pk,lk,format=None):
        self.get_object_like(pk,lk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    