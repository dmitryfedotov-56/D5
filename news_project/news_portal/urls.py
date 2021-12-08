from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostDelete, PostUpdate, upgrade_me
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', PostList.as_view(), name = 'post_list'),
    path('show/<int:pk>', PostDetail.as_view(), name = 'post_detail'),
    path('create/', PostCreate.as_view(), name='create_post'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete_post'),
    path('update/<int:pk>', PostUpdate.as_view(), name='update_post'),
    path('logout/', LogoutView.as_view(template_name='news_portal/logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade'),
]

