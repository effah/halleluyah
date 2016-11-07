import uuid
from phonenumber_field.modelfields import PhoneNumberField
from sortedm2m.fields import SortedManyToManyField
from separatedvaluesfield.models import SeparatedValuesField
from django_comments.models import CommentAbstractModel 
from s3direct.fields import  S3DirectField
from django.db import models

class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	phone = PhoneNumberField(blank=True)
	email = models.EmailField(max_length=255, unique=True,null=False)
	thumbnail = S3DirectField(dest='userProfile', blank=True)
	cover_photo = S3DirectField(dest='userCover', blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class Photo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  
	photo = S3DirectField(dest='userPhotos')
	thumbnail = S3DirectField(dest='userPhotos')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class Bible(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.CharField(max_length=50)
	chapter = models.PositiveSmallIntegerField()
	verses = SeparatedValuesField(max_length=50,cast=int,token=',',choices=((1,'start'),(1,'end')))
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

VOTE_CHOICES = (
    (+1, '+1'),
    (-1, '-1'),
)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updown_votes")
	vote = models.SmallIntegerField(choices=VOTE_CHOICES)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class CommentBox(CommentAbstractModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
		
class Post(models.Model):
	id = models.BigAutoField(primary_key=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	message = models.TextField()
	gallery = SortedManyToManyField(Photo)
	quotation = SortedManyToManyField(Bible)
	likes = SortedManyToManyField(Like)
	comments = SortedManyToManyField(CommentBox)
	created = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
		