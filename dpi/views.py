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
from .models import Patient,UserCredentials,Dpi,Nurse,Administrative,Doctor,Radiologist,Laborantin,Hospital
from .serializers   import PatientSerializer,DoctorSerializer,RadiologistSerializer,NurseSerializer,AdministrativeSerializer
from django.contrib.contenttypes.models import ContentType
from .backends import generate_password , send_password_email





class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})




class CreateHospitalView(APIView):
    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            address = data.get('address')

            # Validate the required fields
            if not name or not address:
                return Response({'status': 'error', 'message': 'Name and address are required'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if a hospital with the same name 
            if Hospital.objects.filter(name=name).exists():
                return Response({'status': 'error', 'message': 'A hospital with this name already exists'},
                                status=status.HTTP_400_BAD_REQUEST)


            hospital = Hospital.objects.create(
                name=name,
                address=address
            )

            return Response({
                'status': 'success',
                'message': 'Hospital created successfully',
                'data': {
                    'id': hospital.id,
                    'name': hospital.name,
                    'address': hospital.address,
                    'created': hospital.created
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': f'An error occurred: {str(e)}'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return Response({'status': 'error', 'message': 'Only POST method is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)






class RegisterPatientView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')

            if UserCredentials.objects.filter(email=email).exists():
                return Response({'status': 'error', 'message': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate email format
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError:
                return Response({'status': 'error', 'message': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate password
            password = generate_password()
            # Hash the password
            hashed_password = make_password(password)

            hospital_name = data.get('hospital')
            hospital = None
            if hospital_name:
                try:
                    hospital = Hospital.objects.get(name=hospital_name)
                except Hospital.DoesNotExist:
                    return Response({'status': 'error', 'message': 'Hospital not found'}, status=status.HTTP_400_BAD_REQUEST)


            patient = Patient.objects.create(
                address=data.get('address'),
                name=data.get('name'),
                phoneNumber=data.get('phoneNumber'),
                SSN=data.get('SSN'),
                dateOfBirth=data.get('dateOfBirth'),
                gender=data.get('Gender'),
                emergencyContactName=data.get('emergencyContactName'),
                emergencyContactPhone=data.get('emergencyContactPhone'),
                email=email
            )


            if hospital:
                hospital.patients.add(patient)


            credentials = UserCredentials.objects.create(
                content_type=ContentType.objects.get_for_model(Patient),
                object_id=patient.id,
                email=email,
                password=hashed_password
            )

            dpi = Dpi.objects.create(patient=patient)

            # Send email
            try:
                send_password_email(email, password)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(credentials)
            access_token = str(refresh.access_token)

            # Return success response
            return Response({
                'status': 'success',
                'message': 'Patient registration successful',
                'data': {
                    'id': patient.id,
                    'name': patient.name,
                    'email': email,
                    'dpi_id': dpi.id,
                    'hospital_id':hospital.id,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': access_token
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return Response({'status': 'error', 'message': 'Only POST method is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)






class RegisterWorkerView(APIView):
    def post(self, request):
        data = request.data

        role = data.get('role')
        email = data.get('email')
        hospital_name = data.get('hospital')

        worker_roles = {
            'doctor': Doctor,
            'nurse': Nurse,
            'administrative': Administrative,
            'radiologist': Radiologist,
            'laborantin': Laborantin,
        }
        worker_model = worker_roles.get(role)

        if not worker_model:
            return Response({'status': 'error', 'message': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        if UserCredentials.objects.filter(email=email).exists():
            return Response({'status': 'error', 'message': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            # Fetch hospital if provided
            if hospital_name:
                try:
                    hospital = Hospital.objects.get(name=hospital_name)
                except Hospital.DoesNotExist:
                    return Response({'status': 'error', 'message': 'Hospital not found'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                hospital = None
            # Prepare common worker data
            worker_data = {
                'name': data.get('name'),
                'phoneNumber': data.get('phoneNumber'),
                'SSN': data.get('SSN'),
                'email': email,
                'hospital': hospital  

            }

            # Handle doctor-specific field
            if role == 'doctor':
                specialty = data.get('specialty')
                if not specialty:
                    return Response({'status': 'error', 'message': 'Specialty is required for doctors'}, status=status.HTTP_400_BAD_REQUEST)
                worker_data['specialty'] = specialty

            worker = worker_model.objects.create(**worker_data)

            # Generate password
            password = generate_password()
            hashed_password = make_password(password)
            credentials = UserCredentials.objects.create(
                content_type=ContentType.objects.get_for_model(worker_model),
                object_id=worker.id,
                email=email,
                password=hashed_password,
            )
            
            # Send email
            try:
                send_password_email(email, password)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(credentials)
            access_token = str(refresh.access_token)

            # Return success response
            return Response({
                'status': 'success',
                'message': f'{role.capitalize()} registered successfully',
                'data': {
                    'id': worker.id,
                    'name': worker.name,
                    'email': email,
                    'role': role,
                    'hospital': hospital.name if hospital else None,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': access_token
                    }
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': f'Error registering {role}: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return Response({'status': 'error', 'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user_credentials = UserCredentials.objects.get(email=email)
            except UserCredentials.DoesNotExist:
                return Response({'status': 'error', 'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

            # Check the password
            if not check_password(password, user_credentials.password):
                return Response({'status': 'error', 'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

            # Identify the actor's role
            actor = user_credentials.actor
            if isinstance(actor, Patient):
                role = 'patient'
            elif isinstance(actor, Doctor):
                role = 'doctor'
            elif isinstance(actor, Administrative):
                role = 'administrative'
            elif isinstance(actor, Nurse):
                role = 'nurse'
            elif isinstance(actor, Radiologist):
                role = 'radiologist'
            elif isinstance(actor, Laborantin):
                role = 'laborantin'
            else:
                role = 'unknown'

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user_credentials)
            refresh['role'] = role  # Add role to the token
            refresh['actor_id'] = actor.id  # Add actor ID to the token

            return Response({
                'status': 'success',
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': role,
                'actor_id': actor.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return Response({'status': 'error', 'message': 'Only POST method is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





class PatientListView(APIView):
    def get(self, request):
        # Get the hospital name from query parameters
        hospital_name = request.query_params.get('hospital')

        if not hospital_name:
            return Response({'status': 'error', 'message': 'Hospital name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response({'status': 'error', 'message': 'Hospital not found'}, status=status.HTTP_404_NOT_FOUND)

        patients = Patient.objects.filter(hospital=hospital)

        serializer = PatientSerializer(patients, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)





class PatientDetailView(APIView):
    def get(self, request, pk):
        try:
            patient = Patient.objects.get(id=pk)  
        except Patient.DoesNotExist:
            return Response({'status': 'error', 'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientSerializer(patient)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    



class Search_by_SSN (APIView):
    def get(self,request,SSN):
        try : 
            patient = Patient.objects.get(SSN=SSN)
        except Patient.DoesNotExist:
            return Response({'status': 'error', 'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientSerializer(patient)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    




class Edit_patient_info (APIView):
    def put(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({'status': 'error', 'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Use partial=True to allow partial updates.
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Patient information updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        




class GetAllWorkersView(APIView):
    def get(self, request):
        # Get the hospital name from the query parameters
        hospital_name = request.query_params.get('hospital', None)

        if not hospital_name:
            return Response({'status': 'error', 'message': 'Hospital name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response({'status': 'error', 'message': 'Hospital not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter workers based on the hospital
        doctors = Doctor.objects.filter(hospital=hospital)
        nurses = Nurse.objects.filter(hospital=hospital)
        radiologists = Radiologist.objects.filter(hospital=hospital)
        administrative_workers = Administrative.objects.filter(hospital=hospital)

        # Serialize the data for each worker type
        doctor_serializer = DoctorSerializer(doctors, many=True)
        nurse_serializer = NurseSerializer(nurses, many=True)
        radiologist_serializer = RadiologistSerializer(radiologists, many=True)
        administrative_serializer = AdministrativeSerializer(administrative_workers, many=True)

        # Combine the serialized data into one response
        combined_data = {
            'doctors': doctor_serializer.data,
            'nurses': nurse_serializer.data,
            'radiologists': radiologist_serializer.data,
            'administrative': administrative_serializer.data,
        }

        return Response({
            'status': 'success',
            'data': combined_data
        }, status=status.HTTP_200_OK)
