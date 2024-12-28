import jwt
from django.conf import settings
from django.http import JsonResponse


from dpi.models import *
from dpi.serializers import *

# def authenticate(request):
#     user = {}
#     user["id"] = 5
#     user["name"] = "Dr.Doktor"
#     user["role"] = "doctor"


#     request.user = user




def authenticate(request):
    """
    Decodes the JWT token from the Authorization header and appends user info to request.
    """
    auth_header = request.headers.get('Authorization', None)
    role_model_dict = {
        "radiologist": Radiologist,
        "patient": Patient,
        "doctor": Doctor,
        "administrative": Administrative,
        "laborantin": Laborantin,
        "nurse": Nurse
    }
    role_serializer_dict = {
        "radiologist": RadiologistSerializer,
        "patient": PatientSerializer,
        "doctor": DoctorSerializer,
        "administrative": AdministrativeSerializer,
        "laborantin": LaborantinSerializer,
        "nurse": NurseSerializer
    }
    if auth_header:
        try:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Extract the token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                
                # Append user info to the request object
                userQuery = role_model_dict[payload.get("role")].objects.get(pk=payload.get("actor_id"))
                user = role_serializer_dict[payload.get("role")](userQuery).data

                request.user = user
                
                

            else:
                return JsonResponse({"error": "Invalid authorization header"}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
    else:
        return JsonResponse({"error": "Authorization header not found"}, status=401)

    return None
