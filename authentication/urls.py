
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', SigninView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('profile/<int:pk>/',ProfileView.as_view(),name='profile')
]