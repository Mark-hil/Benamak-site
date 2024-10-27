from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)


class Product(models.Model):
    name =models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    image = models.FileField()
    # category = models.ForeignKey(Category, related_name='product')



class PortfolioItem(models.Model):
    CATEGORY_CHOICES = [
        ('App', 'App'),
        ('Card', 'Card'),
        ('Web', 'Web'),
    ]
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/portfolio/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    t_shirt_type = models.CharField(max_length=255)
    design = models.ImageField(upload_to='designs/')
    message = models.TextField()

    def __str__(self):
        return self.name
