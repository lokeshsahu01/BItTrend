from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', register_view),
    path('login/', user_login_view),
    path('kyc/update', user_profile_view),
]
