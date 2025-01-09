from django.urls import path
from .views import (
    UserRegistrationView,
    UserListView,
    ObtainTokenPairView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('list/', UserListView.as_view(), name='user_list'),
]