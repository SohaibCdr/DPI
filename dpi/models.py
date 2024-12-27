from django.db import models
from datetime import date
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber =  models.CharField(max_length=10)                   # blank=True, null=True
    SSN = models.CharField(max_length=50 , unique=True,null=False)
    dateAdded = models.DateTimeField(auto_now_add=True,null=True)
    email = models.CharField(max_length=50, unique=True,null=True)

    def __str__(self):
        return self.name	
    
    class Meta:
        ordering = ['-dateAdded']
        abstract = True  # This makes it an abstract model


class  Administrator (Actor):
    pass


class Hospital(models.Model):
    name= models.CharField(max_length=50,unique=True)
    address= models.CharField(max_length=100,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    admin = models.ForeignKey(Administrator, on_delete=models.SET_NULL, null=True, related_name='managed_hospitals')
    # Counter fields for workers
    doctor_count = models.IntegerField(default=0)
    nurse_count = models.IntegerField(default=0)
    administrative_count = models.IntegerField(default=0)
    radiologist_count = models.IntegerField(default=0)
    laborantin_count = models.IntegerField(default=0)
    def __str__(self):
        return self.name  

class Doctor(Actor):
    specialty = models.CharField(max_length=100) 
    hospital = models.ForeignKey(
        Hospital,
        related_name='doctors',  # Unique related_name
        on_delete=models.SET_NULL,
        null=True
    )


class Patient(Actor):
    address =models.CharField(max_length=200, null=False,default="paitent adress")
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







class Dpi (models.Model):
    createdAt = models.DateTimeField(auto_now_add=True,null=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    def __str__(self):
        return f"DPI of {self.patient.user.username}"
    

class prescription (models.Model):
    issueDate = models.CharField(max_length=10)
    validationDate=models.CharField(max_length=10)
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)
    def __str__(self):
        return f"Prescription for {self.dpi.patient.user.username}"


class Care (models.Model):
    observation = models.CharField(max_length=500)
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)
    def __str__(self):
        return f"Prescription for {self.dpi.patient.user.username}"



class   MedicalCondition (models.Model):
    date=models.CharField(max_length=10)
    type= models.CharField(max_length=100)
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)
    def __str__(self):
        return f"Condition for {self.dpi.patient.user.username}"



# Test model (now with type differentiation)
class Test(models.Model):
    TEST_TYPES = (
        ('bloodwork', 'Bloodwork'),
        ('scan', 'Scan'),
    )
    type = models.CharField(max_length=50, choices=TEST_TYPES)
    issueDate = models.DateField()
    conductionDate = models.DateField()
    status = models.CharField(max_length=10)
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} test for {self.dpi.patient.user.username}"



# Bloodwork model (if still needed)
class Bloodwork(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name="bloodwork")
    results = models.TextField()


# Scan model (if still needed)
class Scan(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name="scan")
    image = models.ImageField(upload_to='examinations/', blank=True, null=True)
    