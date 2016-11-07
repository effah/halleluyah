import uuid
from phonenumber_field.modelfields import PhoneNumberField
from sortedm2m.fields import SortedManyToManyField
from separatedvaluesfield.models import SeparatedValuesField
from django_comments.models import CommentAbstractModel
from updown.models import Vote
from django.db import models

class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	phone = PhoneNumberField(blank=True)
	email = models.EmailField(max_length=255, unique=True,null=False)
	thumbnail = models.CharField(max_length=255)
	cover_photo = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class Photo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  
	photo = models.CharField(max_length=255)
	thumbnail =models.CharField(max_length=255)

class Bible(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.CharField(max_length=50)
	chapter = models.PositiveSmallIntegerField()
	verses = SeparatedValuesField(max_length=50,cast=int,token=',',choices=((1,'start'),(1,'end')))

class Like(Vote):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updown_votes")

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
		