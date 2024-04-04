
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login/', SigninView.as_view(), name="login"),
    # path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignupView.as_view(), name="signup"),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})',
    #     activate, name='activate'),
    path('profile/<int:pk>/',ProfileView.as_view(),name='profile'),
    path('change_username/<int:pk>/',ChangeInformationView.as_view(),name='change-username'),
    # path('change_biography/<int:pk>/',ChangeBiographyView.as_view(),name='change-bio'),
    # path('change_hobbies/<int:pk>/',ChangeHobbiesView.as_view(),name='change-hobbies'),
    # path('settings/<int:pk>/', SettingsView.as_view(), name='settings'),
    path('resetpass/',UsersResetPasswordView.as_view(),name='reset_password'),
    path('resetpass/done/',UsersPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('passconfirm/<uidb64>/<token>/',UsersConfirmNewPasswordView.as_view(),name='password_reset_confirm'),
    path('passconfirm/complete',UsersCompletePasswordChangeView.as_view(),name='complete_password_change'),


]