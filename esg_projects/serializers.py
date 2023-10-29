from rest_framework import serializers
from .models import ESGProject, UserTask


class ESGProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESGProject
        fields = '__all__'


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'
