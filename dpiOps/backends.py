def authenticate(request):
    user = {}
    user["actor_id"] = 5
    user["name"] = "Dr.Doktor"
    user["role"] = "doctor"


    request.user = user

