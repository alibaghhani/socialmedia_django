from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('',HomepageView.as_view(),name='home'),
    path('explore/', TemplateView.as_view(template_name='explore.html'), name='explore'),
    path('post/',post_upload,name='post'),
    path('search/',SearchUsersView.as_view(),name='search-users'),
    path('like/<int:pk>',LikePostView,name='like_post'),
    # path('dislike/<int:pk>/',PostDisLikeView.as_view(),name='like_post'),
    path('postdisplay/<int:pk>/',PostDisplayView.as_view(),name='post_display'),
    path('users/',UsersListView.as_view(),name='users_list'),
    path('follow/<int:user_id>/',FollowView.as_view(),name='follow'),
    path('unfollow/<int:user_id>/',UnfollowView.as_view(),name='unfollow'),
    path('post_detail/<int:pk>',PostDetail.as_view(),name='post_detail'),
    path('comment/',CreateCommentView.as_view(),name='comment'),
    path('edit_post/<int:pk>/',EditPostView.as_view(),name='edit-post')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)