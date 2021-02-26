from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    #path('api-token-auth/', obtain_auth_token, name='authentication'),
    path('api-token-auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    #path('api/lists/', views.ListCollectionView.as_view(), name='getAllLists'),
    path(
        'api/lists/', 
        views.ListViewSet.as_view({
            'get': 'list'
        }),
        name='getAllLists',
    ),
    path(
        'api/list/', 
        views.ListViewSet.as_view({
            'post': 'create'
        }),
        name='createList'
    ),
    path(
        'api/list/<int:id>/', 
        views.ListViewSet.as_view({
            'get': 'retrieve',
            'patch': 'update_partial',
            'delete': 'destroy',
        }),
        name='listOperations'
    ),



    #TASKS-----------
    path(
        'api/tasks/<int:list_id>/', 
        views.TaskViewSet.as_view({
            'get': 'list',
        }),
        name='getAllTasksOfList'
    ),

    path(
        'api/task/<int:list_id>/',
        views.TaskViewSet.as_view({
            'post': 'create',
        }),
        name='createTask'
    ),

    path(
        'api/task/<int:list_id>/<int:task_id>/',
        views.TaskViewSet.as_view({
            'get': 'retrieve',
            'patch': 'update_partial',
            'delete': 'destroy'
        }),
        name='taskOperations'
    ),




    path(
        'api/register/',
        views.UserViewSet.as_view({
            'post': 'create',
        }),
        name='userRegistration'
    ),



]