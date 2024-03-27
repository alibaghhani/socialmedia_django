from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('',HomepageView.as_view(),name='home'),
    path('explore/', TemplateView.as_view(template_name='explore.html'), name='explore'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='settings'),
    path('post/',UploadPostView.as_view(),name='post')


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)