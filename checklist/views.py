from rest_framework import viewsets
from checklist.models import List, Task
from checklist.serializers import ListSerializer, TaskSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import exceptions
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.db.models import Q


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

    def list(self, request, list_id, page):

        listObj=getList(list_id, request.user)
        if isinstance(listObj, Response):
            return listObj

        ordering = getattr(listObj, 'order')
        if ordering == 'Time':
            tasks =  Task.objects.filter(checklist=listObj).order_by(Coalesce('date', 'time').asc(nulls_last=True))    
        elif ordering == '-Time':
            tasks =  Task.objects.filter(checklist=listObj).order_by('-date', '-time')    
        elif ordering == '-Name':
            tasks =  Task.objects.filter(checklist=listObj).order_by('-name')    
        else:
            tasks =  Task.objects.filter(checklist=listObj).order_by('name')    
        
        p = Paginator(tasks, 5)
        if p.num_pages < page or page<=0:
            return Response(data={'message': 'Page number not valid.'} ,status=404)

        serializer = TaskSerializer(p.page(page).object_list, many=True)

        res = {
            'order':ordering,
            'pages': p.num_pages
        }
        res.update({'tasks':serializer.data})

        return Response(res, status=200)
    
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


class DeadlineViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        tasks =  Task.objects.filter(Q(checklist__user=request.user), (Q(date__isnull=False) | Q(time__isnull=False)))
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=200)






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
