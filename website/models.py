from django.db import models
from dashboard.models import *

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blog_images")
    text =  models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
        
class About(models.Model):
    message = models.TextField()
    def __str__(self):
        return self.message


    
class Testimony(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to="test_images")


    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    review = models.TextField()
    rate = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
