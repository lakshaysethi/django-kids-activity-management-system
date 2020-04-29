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



def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

class Activity(models.Model):
  name = models.CharField(max_length=255)
  start_time = models.DateTimeField()
  duration = models.DurationField(default='01:00:00')
  def dur_str(self):
    return strfdelta(self.duration, "{hours} Hours and {minutes} Minutes")


  def __str__(self):
    return self.name


class Child(models.Model):
  name = models.CharField(max_length=50)
  # age = models.IntegerField()
  date_of_birth = models.DateField()
  address = models.CharField(max_length=255)
  contact = models.CharField(max_length=15)
  enrolled_activities = models.ManyToManyField(Activity,blank=True)

  def __str__(self):
    return self.name


class User(AbstractUser):
  roles = models.ManyToManyField(Role)
  myChildren = models.ManyToManyField(Child,blank=True)

  def __str__(self):
    return self.username

