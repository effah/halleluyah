import uuid, os
from phonenumber_field.modelfields import PhoneNumberField
from sortedm2m.fields import SortedManyToManyField
from separatedvaluesfield.models import SeparatedValuesField
from django_comments.models import CommentAbstractModel 
from django.db import models
from functools import partial 
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User

def _update_filename(instance, filename, path):
	path = path
	ext = filename.split('.')[-1] 
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join(path, filename)

def get_file_path(path):
	return partial(_update_filename, path=path)

class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	phone = PhoneNumberField(blank=True)
	email = models.EmailField(max_length=255, unique=True,null=False)
	thumbnail = models.FileField(upload_to=get_file_path('profile-photos'), blank=True)
	cover_photo = models.FileField(upload_to=get_file_path('cover-photos'), blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ('id',)
	
	# Add some custom validation to our image field
	def clean_image(self): 
		max_size = 4*1024*1024
		if self.thumbnail:
			if self.thumbnail.size > max_size:
				raise ValidationError("Thumbnail Image file too large ( > 4mb )")
		elif self.cover_photo:
			if self.cover_photo.size > max_size:
				raise ValidationError("Cover Photo Image file too large ( > 4mb )")

class Photo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  
	photo = models.FileField(upload_to=get_file_path('photos'))
	thumbnail = models.FileField(upload_to=get_file_path('photos'), blank=True)
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
	gallery = SortedManyToManyField(Photo, blank=True)
	quotation = SortedManyToManyField(Bible, blank=True)
	likes = SortedManyToManyField(Like, blank=True)
	comments = SortedManyToManyField(CommentBox, blank=True)
	created = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
		