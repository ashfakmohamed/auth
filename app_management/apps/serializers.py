from rest_framework import serializers
from .models import App, Task

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'link', 'category', 'sub_category', 'points']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'app', 'screenshot', 'completed']
