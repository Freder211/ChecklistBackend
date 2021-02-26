from checklist.models import List, Task
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        

class ListSerializer(serializers.ModelSerializer):

    checkedTasks = serializers.SerializerMethodField()
    totalTasks = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ['id', 'name', 'order', 'checkedTasks', 'totalTasks']

    def get_checkedTasks(self, obj):
        return Task.objects.filter(checklist=obj.id, checked=True).count()

    def get_totalTasks(self, obj):
        return Task.objects.filter(checklist=obj.id).count()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'text',
            'date',
            'time',
            'checked',
            'notified',
        ]
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user