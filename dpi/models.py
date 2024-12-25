from django.db import models
from datetime import date
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Hospital(models.Model):
    name= models.CharField(max_length=50,unique=True)
    address= models.CharField(max_length=100,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    # Counter fields for workers
    doctor_count = models.IntegerField(default=0)
    nurse_count = models.IntegerField(default=0)
    administrative_count = models.IntegerField(default=0)
    radiologist_count = models.IntegerField(default=0)
    laborantin_count = models.IntegerField(default=0)
    def __str__(self):
        return self.name   


class Actor(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber =  models.CharField(max_length=10)                   # blank=True, null=True
    SSN = models.CharField(max_length=50 , unique=True)
    dateAdded = models.DateTimeField(auto_now_add=True,null=True)
    email = models.CharField(max_length=50, unique=True,null=True)

    def __str__(self):
        return self.name	
    
    class Meta:
        ordering = ['-dateAdded']
        abstract = True  # This makes it an abstract model


class Doctor(Actor):
    specialty = models.CharField(max_length=100) 
    hospital = models.ForeignKey(
        Hospital,
        related_name='doctors',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )


class Patient(Actor):
    address =models.CharField(max_length=200,null=True)
    gender=models.CharField(max_length=10)
    dateOfBirth = models.DateField(null=True)
    emergencyContactName = models.CharField(max_length=50, null=True)
    emergencyContactPhone= models.CharField(max_length=10, null=True)
    updated = models.DateTimeField(auto_now=True)
    hospital = models.ForeignKey(
        Hospital,
        related_name='patients',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )	
    @property
    def age(self):
        if self.dateOfBirth:
            today = date.today()
            return today.year - self.dateOfBirth.year - (
                (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day)
            )
        return None
    

class  Administrative (Actor):
    hospital = models.ForeignKey(
        Hospital,
        related_name='administratives',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )

class  Nurse (Actor):
    hospital = models.ForeignKey(
        Hospital,
        related_name='nurses',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )


class  Radiologist (Actor):
    hospital = models.ForeignKey(
        Hospital,
        related_name='radilogists',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )


class  Laborantin (Actor):
    hospital = models.ForeignKey(
        Hospital,
        related_name='laborantins',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )



class UserCredentials(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('content_type', 'object_id')
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)







