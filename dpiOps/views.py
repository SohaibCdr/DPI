import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

from .models import *
from dpi.models import *
from dpi.serializers import *
from .serializers import *
from .backends import *
# Create your views here.

@api_view(['GET'])
def get_medical_history(request,SSN):
    patient = {}
    try:
        patient = Patient.objects.get(SSN=SSN)

    except Patient.DoesNotExist:
        return JsonResponse({
            "status": "failed",
            "message": "Patient does not exist",
        },
        status=404
        )
    medicalHistoryQuery = MedicalCondition.objects.select_related("doctor").filter(patient=patient)

    #check if the results aren't empty
    medicalHistory = {}
    if medicalHistoryQuery:
        medicalHistory = MedCondSerializer(medicalHistoryQuery, many=True).data
    #get the doctor name that treated the conditions
    for condition in medicalHistory:
        condition["doctor"] = DoctorSerializer(Doctor.objects.get(pk=condition["doctor"])).data["name"]
        

    return JsonResponse({
        "status": "success",
        "data": medicalHistory

    },status=200)

        
@api_view(["POST"])
def add_medical_condition(request,patient_pk):
    authenticate(request=request)
    try:
        patient = {}
        try:
            patient = Patient.objects.get(pk=patient_pk)

        except Patient.DoesNotExist:
            return JsonResponse({
                "status": "failed",
                "message": "Patient does not exist",
            },
            status=404
            )
        if (not request.data.get('reason')):
            return JsonResponse({
                "status": "failure",
                "message": "must provide a reason for the new dpi page"
                },
                status=400)
        
        medicalCondition = MedCondSerializer(MedicalCondition.objects.create(
        reason = request.data.get('reason'),
        patient = patient,
        doctor = Doctor.objects.get(pk=request.user.get("actor_id"))
        )).data

        return JsonResponse({
            "status": "success",
            "data":
                medicalCondition
        })
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': f'An error occurred: {str(e)}'},
            status =500
            ) 

@api_view(['POST'])    
def edit_medical_condition_page(request, pk):
    try:
        # Retrieve the MedicalCondition object
        medicalCondition = MedicalCondition.objects.get(pk=pk)
        
        # Check if request data contains values and update accordingly
        if 'resume' in request.data:
            medicalCondition.resume = request.data['resume']
        
        if 'reason' in request.data:
            medicalCondition.reason = request.data['reason']
        
        # Save the object after updating fields
        medicalCondition.save()

        return JsonResponse({
            "status": "success",
            "message": "Medical condition page updated successfully"
        }, status=204)
    
    except MedicalCondition.DoesNotExist:
        # Return failure response if object doesn't exist
        return JsonResponse({
            "status": "failure",
            "message": "The medical condition page does not exist"
        }, status=404)

    
