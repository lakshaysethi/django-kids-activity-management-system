from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Role(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    TEACHER = 1
    PARENT = 2

    ROLE_CHOICES = (
        (PARENT, 'parent'),
        (TEACHER, 'teacher'),

    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class Activity(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=50)
    # age = models.IntegerField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    enrolled_activities = models.ManyToManyField(
        Activity, blank=True)


class User(AbstractUser):
    roles = models.ManyToManyField(Role)
    myChildren = models.ManyToManyField(Child, blank=True)

    def __str__(self):
        return self.username
