from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

STATUS_CHOICE = (
    ('draft', 'draft'),
    ('published', 'published')
)


class User(AbstractUser):
    pass


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Customer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='customer', default=1)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
