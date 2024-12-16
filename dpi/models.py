from django.db import models
from datetime import date


# Create your models here.


class Hospital(models.Model):
    name= models.CharField(max_length=50,unique=True)
    address= models.CharField(max_length=100,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
    


class Actor(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber =  models.CharField(max_length=10)                   # blank=True, null=True
    email= models.CharField(max_length=50,unique=True,null=True)
    SSN = models.CharField(max_length=50)
      #Always hash passwords using Django's make_password() or authentication system.
    dateAdded = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    password = models.CharField(max_length=128,null=True)

    def __str__(self):
        return self.name	
    
    class Meta:
        ordering = ['-created']
        abstract = True  # This makes it an abstract model


class Doctor(Actor):
	specialty = models.CharField(max_length=100) 
     

class Patient(Actor):
    gender=models.CharField(max_length=10)
    dateOfBirth = models.CharField(max_length=10)
    emergencyContactName = models.CharField(max_length=50,blank=True, null=True)
    emergencyContactPhone= models.CharField(max_length=10,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)	
    #dpi = 
    @property
    def age(self):
        if self.dateOfBirth:
            today = date.today()
            return today.year - self.dateOfBirth.year - (
                (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day)
            )
        return None
    class Meta:
        ordering = ['-updated', '-created']



from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserCredentials(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('content_type', 'object_id')
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)