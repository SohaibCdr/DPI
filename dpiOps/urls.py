from django.urls import path
from .views import *

urlpatterns = [
    path("api/medicalHistory/<str:SSN>", get_medical_history, name="get_medical_history"),
    path("api/medicalHistory/add/<int:patient_pk>", add_medical_condition, name="add_medical_condition"),
    path("api/medicalHistory/edit/<int:pk>", edit_medical_condition_page, name="edit_medical_condition_page")
]