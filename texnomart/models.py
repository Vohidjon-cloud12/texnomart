from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        get_latest_by = 'updated_at'
        ordering = ['-created_at']


class Category(TimeStampedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.title


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.FloatField()
    description = models.TextField()
    user_like = models.ManyToManyField(User, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    discount = models.FloatField(blank=True,default=0)


    def __str__(self):
        return self.name

    @property
    def discounted_price(self) :
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100))
        return self.price

    @property
    def rasroch_price(self):
            return self.discounted_price / 24


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Product, self).save(*args, **kwargs)


class AttributeKey(models.Model):
    key_name = models.CharField(max_length=100)

    def __str__(self):
        return self.key_name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class Attribute(models.Model):
    attribute_key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE,related_name='attributes')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,related_name='values')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')


class Image(models.Model):
    image = models.ImageField(upload_to='images/products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name




class Comments(models.Model):
    class Rating(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    rating = models.IntegerField(choices=Rating.choices, default=Rating.One.value)
    def __str__(self):
        return self.comment

