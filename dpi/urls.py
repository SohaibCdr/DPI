from django.urls import path
from .views import ProtectedView,PatientListView,GetAllWorkersView,CreateHospitalView,PatientDetailView,Search_by_SSN,Edit_patient_info,RegisterWorkerView,LoginView,RegisterPatientView
from .views import GetHospitalView,UpdateWorkerView,DeleteWorkerView
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/hospital/create/', CreateHospitalView.as_view(), name='create_hospital'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/patient/', RegisterPatientView.as_view(), name='register_patient'),
    path('api/patients/', PatientListView.as_view(), name='patient-list'),
    path('api/patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('api/search/<str:SSN>/',Search_by_SSN.as_view(), name="search_by_SSN"),
    path('api/patient/edit/<int:pk>/', Edit_patient_info.as_view(), name='edit_patient'),
    path('api/register/worker/',RegisterWorkerView.as_view(), name='register_worker'),
    path('api/workers/', GetAllWorkersView.as_view(), name='get_all_workers'),
    path('api/hospital/', GetHospitalView.as_view(), name='get_hospital'),
    path('api/worker/edit/', UpdateWorkerView.as_view(), name='update_worker'),
    path('api/worker/delete', DeleteWorkerView.as_view(), name='delete-worker'),
]