# Serializer for tasks models

from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        
        # fields = (
        #     'id',
        #     'title',
        #     'description',
        #     'completed',
        # )
        fields = '__all__'

        read_only_fields = ('id',)