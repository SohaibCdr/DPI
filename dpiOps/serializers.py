
from rest_framework import serializers
from dpiOps.models import *


class MedCondSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCondition
        fields = "__all__"

class MedCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Care
        fields = "__all__"