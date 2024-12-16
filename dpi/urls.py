from django.urls import path
from .views import ProtectedView,PatientListView,PatientDetailView
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('api/login/', views.login_view, name='login'),
    path('api/register/patient/', views.register_patient, name='register_patient'),
    path('api/patients/', PatientListView.as_view(), name='patient-list'),
    path('api/patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
]