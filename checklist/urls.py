from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='authentication'),

    path('api/lists/', views.ListCollectionView.as_view(), name='getAllLists'),
    path('api/list/', views.ListElementView.as_view(), name='createList'),
    path('api/list/<int:id>/', views.ListElementView.as_view(), name='listOperations'),

    path('api/tasks/<str:list_id>/', views.TaskCollectionView.as_view(), name='getAllTasksOfList'),
    path('api/task/<str:list_id>/', views.TaskElementView.as_view(), name='creatTask'),
    path('api/task/<str:list_id>/<str:task_id>/', views.TaskElementView.as_view(), name='taskOperations'),
]