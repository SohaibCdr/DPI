from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phoneNumber', 'gender', 
            'dateOfBirth', 'emergencyContactName', 'emergencyContactPhone'
        ]