from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from .models import Patient,Doctor
from django.contrib.auth.hashers import make_password,check_password
import json
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient,UserCredentials
from .serializers   import PatientSerializer
from django.contrib.contenttypes.models import ContentType

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})

@csrf_exempt  # Disable CSRF for testing with Postman (ensure you handle it properly in production)
def register_patient(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        password = data.get('password')  
        email = data.get('email')

        if Patient.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already in use'}, status=400)
        
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Invalid email format'}, status=400)
        hashed_password = make_password(password)
    
        patient = Patient(
            password=hashed_password,
            name = data.get('name'),
            email=email,
            phoneNumber = data.get('phoneNumber'),
            SSN = data.get('SSN'),
            dateOfBirth = data.get('dateOfBirth'),
            gender = data.get('Gender'),
            emergencyContactName = data.get('emergencyContactName'),
            emergencyContactPhone = data.get('emergencyContactPhone'),
        )
        patient.save()
        credentials = UserCredentials.objects.create(
        content_type=ContentType.objects.get_for_model(Patient),
        object_id=patient.id,
        email=patient.email,
        password=hashed_password
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(patient)
        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Patient registration successful','data': {
        'id': patient.id,
        'name': patient.name,
        'email': patient.email,
    },}, status=201)

    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)










@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'status': 'error', 'message': 'Email and password are required'}, status=400)

            
            try:
                user_credentials = UserCredentials.objects.get(email=email)
            except UserCredentials.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=400)

            
            if not check_password(password, user_credentials.password):
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=400)

            
            actor = user_credentials.actor
            if isinstance(actor, Patient):
                role = 'patient'
            elif isinstance(actor, Doctor):
                role = 'doctor'
            else:
                role = 'unknown'

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user_credentials)  # Generic user
            refresh['role'] = role  # Add role to the token
            refresh['actor_id'] = actor.id  # Add actor-specific ID

            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': role,
                'actor_id': actor.id
            }, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)



class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)




class PatientDetailView(APIView):
    def get(self, request, pk):
        try:
            patient = Patient.objects.get(id=pk)  # Replace `id` with another field if needed
        except Patient.DoesNotExist:
            return Response({'status': 'error', 'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientSerializer(patient)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    



