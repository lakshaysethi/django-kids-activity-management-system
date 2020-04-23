from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Role(models.Model):
 
  PARENT = 2
  TEACHER = 1
  
  ROLE_CHOICES = (
      (PARENT, 'parent'),
      (TEACHER, 'teacher'),
      
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()


class User(AbstractUser):
  roles = models.ManyToManyField(Role)