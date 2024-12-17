from django.db import models
from datetime import date
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    SSN = models.CharField(max_length=50)
    dateAdded = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    email = models.CharField(max_length=50, unique=True , null=True)

    def __str__(self):
        return self.name	
    
    class Meta:
        ordering = ['-created']
        abstract = True  # This makes it an abstract model


class Doctor(Actor):
	specialty = models.CharField(max_length=100) 
     

class Patient(Actor):
    gender=models.CharField(max_length=10)
    dateOfBirth = models.DateField(null=True, blank=True)
    emergencyContactName = models.CharField(max_length=50,blank=True, null=True)
    emergencyContactPhone= models.CharField(max_length=10,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)	
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

class  Administrative (Actor):
    pass



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
    dpi = models.OneToOneField(Dpi, on_delete=models.CASCADE)
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
    