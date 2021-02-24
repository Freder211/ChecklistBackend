from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    #path('api-token-auth/', obtain_auth_token, name='authentication'),
    path('api-token-auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('api/lists/', views.ListCollectionView.as_view(), name='getAllLists'),
    path('api/list/', views.createList, name='createList'),
    path('api/list/<int:id>/', views.ListElementView.as_view(), name='listOperations'),

    path('api/tasks/<int:list_id>/', views.TaskCollectionView.as_view(), name='getAllTasksOfList'),
    path('api/task/<int:list_id>/', views.TaskElementView.as_view(), name='creatTask'),
    path('api/task/<int:list_id>/<int:task_id>/', views.TaskElementView.as_view(), name='taskOperations'),
    path('api/nTasks/<int:list_id>/', views.nTasks, name='getTaskCount'),

    path('api/register/', views.userCreate, name='createUser'),
    path('api/user/', views.getUser, name='getUser')
]