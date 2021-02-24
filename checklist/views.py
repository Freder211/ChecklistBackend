from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from checklist.models import List, Task
from checklist.serializers import ListSerializer, TaskSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from django.core import exceptions
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
import io

#######helping functions########
def test(request, test):
    print(test)
    return render(request, 'checklist/test.html', {'test' : test})

def getList(id, user):
    try:
        listObj = List.objects.get(user__username=user, id=id)
    except List.DoesNotExist:
        return Response(status=404)
    except exceptions.ValidationError:
        return Response(status=400)
    
    return listObj

def getTask(task_id, list_id, user):

    try:
        task = Task.objects.get(checklist__id=list_id, checklist__user=user, id=task_id)
    except Task.DoesNotExist:
        return Response(status=404)
    except exceptions.ValidationError:
        return Response(status=400)
    
    return task

#######class based views########
class ListCollectionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            lists = List.objects.filter(user__username=request.user)
        except List.DoesNotExist:
            return HttpResponse(status=404)

        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)


class ListCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class ListElementView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        listObj=getList(id, request.user)
        if(isinstance(listObj, Response)):
            return listObj


        serializer = ListSerializer(listObj)
        return Response(serializer.data)

    def patch(self, request, id):
        listObj=getList(id, request.user)
        if(isinstance(listObj, Response)):
            return listObj

        serializer = ListSerializer(listObj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        
        return Response(serializer.errors, status=400)

    
    def delete(self, request, id):
        listObj=getList(id, request.user)
        if(isinstance(listObj, Response)):
            return listObj
        
        listObj.delete()
        return Response(status=204)

class TaskCollectionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, list_id):
        listObj=getList(list_id, request.user)
        if isinstance(listObj, Response):
            return listObj
        
        tasks =  Task.objects.filter(checklist=listObj)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
        


class TaskElementView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, list_id, task_id):
        task=getTask(task_id, list_id ,request.user)
        if isinstance(task, Response):
            return task
        
        serializer = TaskSerializer(task)
        
        return Response(data=serializer.data)
    
    def post(self, request, list_id):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            #####CHIEDERE
            listObj = getList(list_id, request.user)
            if isinstance(listObj, Response):
                return listObj
            

            serializer.save(checklist=listObj)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, list_id, task_id):
        task=getTask(task_id, list_id ,request.user)
        if isinstance(task, Response):
            return task
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)

        return Response(serializer.errors, status=400)

    
    def delete(self, request, list_id, task_id):
        task=getTask(task_id, list_id ,request.user)
        if isinstance(task, Response):
            return task
        
        task.delete()
        return Response(status=204)

########function based views########
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nTasks(request, list_id):
    nTasks = Task.objects.filter(
        checklist__id=list_id,
        checklist__user=request.user
    ).count()
    return Response(data=nTasks, status=200)

@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createList(request):
    serializer = ListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    user = User.objects.get(username=request.user)
    print(user)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)