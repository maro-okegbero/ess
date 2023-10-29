from django.urls import path, include

from .views import login_user, register_as_administrator, create_user_as_admin

urlpatterns = [
        # user actions
        path('register_as_administrator', register_as_administrator, name='register_as_administrator'),
        path('login', login_user, name='login_user'),
        path('create_user_as_admin', create_user_as_admin, name='create_user_as_admin'),
        path('', include('esg_projects.urls')),
]
