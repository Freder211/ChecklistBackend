from rest_framework import viewsets
from checklist.models import List, Task
from checklist.serializers import ListSerializer, TaskSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import exceptions

class UserViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        
        return Response(serializer.errors, status=400)

class ListViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            lists = List.objects.filter(user__username=request.user)
        except List.DoesNotExist:
            return Response(status=404)

        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


    def retrieve(self, request, id):
        listObj=getList(id, request.user)
        if(isinstance(listObj, Response)):
            return listObj


        serializer = ListSerializer(listObj)
        return Response(serializer.data)
    
    def update_partial(self, request, id):
        listObj=getList(id, request.user)
        if(isinstance(listObj, Response)):
            return listObj

        serializer = ListSerializer(listObj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        
        return Response(serializer.errors, status=400)

    def destroy(self, request, id):
        listObj=getList(id, request.user)
        if(isinstance(listObj, Response)):
            return listObj
        
        listObj.delete()
        return Response(status=204)


class TaskViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, list_id):
        print('ciao')
        listObj=getList(list_id, request.user)
        if isinstance(listObj, Response):
            return listObj
        
        tasks =  Task.objects.filter(checklist=listObj)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
    
    def create(self, request, list_id):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            #####CHIEDERE
            listObj = getList(list_id, request.user)
            if isinstance(listObj, Response):
                return listObj
            

            serializer.save(checklist=listObj)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

    
    def retrieve(self, request, list_id, task_id):
        task=getTask(task_id, list_id ,request.user)
        if isinstance(task, Response):
            return task
        
        serializer = TaskSerializer(task)
        
        return Response(data=serializer.data)

    def update_partial(self, request, list_id, task_id):
        task=getTask(task_id, list_id ,request.user)
        if isinstance(task, Response):
            return task
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)

        return Response(serializer.errors, status=400)
    
    def destroy(self, request, list_id, task_id):
        task=getTask(task_id, list_id ,request.user)
        if isinstance(task, Response):
            return task
        
        task.delete()
        return Response(status=204)









#######helping functions########
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
