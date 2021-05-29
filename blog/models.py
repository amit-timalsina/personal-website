from django.db import models
from django.contrib.auth.models import User

from base.models import Profile
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import readtime
# Create your models here.

class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.name)
            self.slug = slug
        super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='images', default='/images/placeholder.png')
    body = RichTextUploadingField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    latest = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.headline
    
    class Meta:
        ordering = ['-created']
        # unique_together = ('user',)
    
    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.headline)

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()
            
            self.slug = slug
        super().save(*args, **kwargs)

class PostComment(models.Model):
    # name = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    website = models.CharField(max_length=100, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body
    
    @property
    def created_dynamic(self):
        now = timezone.now()
        return now
    