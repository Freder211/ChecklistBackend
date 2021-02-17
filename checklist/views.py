from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from checklist.models import List, Task
from checklist.serializers import UserSerializer, GroupSerializer, ListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.core import exceptions
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

def test(request, test):
    print(test)
    return render(request, 'checklist/test.html', {'test' : test})


class ListCollectionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            lists = List.objects.filter(user__username=request.user)
        except List.DoesNotExist:
            return HttpResponse(status=404)

        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

class ListElementView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            lists = List.objects.get(user__username=request.user, id=id)
        except List.DoesNotExist:
            return HttpResponse(status=404)

        serializer = ListSerializer(lists)
        return Response(serializer.data)
