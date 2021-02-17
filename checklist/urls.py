from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/lists/', views.ListCollectionView.as_view(), name='ciao'),
    path('api/lists/<str:id>', views.ListElementView.as_view(), name='list'),
]