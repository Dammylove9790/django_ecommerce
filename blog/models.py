from django.db import models
from django.utils.text import slugify

from store.models import Category
import uuid
# Create your models here.


class Category(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        # verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

class Author(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # class Meta:
    #     verbose_name = 'Author'
    #     verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name
    

class Post(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    slug = models.SlugField(unique=True)
 
