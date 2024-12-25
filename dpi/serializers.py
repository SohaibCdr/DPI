from rest_framework import serializers
from .models import Patient,Doctor, Nurse, Radiologist, Administrative, Actor

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phoneNumber', 'gender', 
            'dateOfBirth', 'emergencyContactName', 'emergencyContactPhone'
        ]



class DoctorSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='doctor', read_only=True)  # Add role for doctor
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'email','phoneNumber', 'SSN', 'dateAdded', 'specialty', 'role']

class NurseSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='nurse', read_only=True)  # Add role for nurse
    
    class Meta:
        model = Nurse
        fields = ['id', 'name','email', 'phoneNumber', 'SSN', 'dateAdded', 'role']

class RadiologistSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='radiologist', read_only=True)  # Add role for radiologist
    
    class Meta:
        model = Radiologist
        fields = ['id', 'name','email', 'phoneNumber', 'SSN', 'dateAdded', 'role']

class AdministrativeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='administrative', read_only=True)  # Add role for administrative
    
    class Meta:
        model = Administrative
        fields = ['id', 'name','email', 'phoneNumber', 'SSN', 'dateAdded', 'role']


class LaborantinSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='administrative', read_only=True)  
    
    class Meta:
        model = Administrative
        fields = ['id', 'name','email', 'phoneNumber', 'SSN', 'dateAdded', 'role']
