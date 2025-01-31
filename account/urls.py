from django.urls import path
from .import views
from .views import role_based_redirect


app_name = 'account'
urlpatterns = [

    path('role-based-redirect/', role_based_redirect, name='role_based_redirect'),
    path('user_management/', views.UserManagementView.as_view(), name='user_management'),
    path('assign_to_group/<int:user_id>/', views.AssignToGroupView.as_view(), name='assign_to_group'),
    path('view_users_in_group/', views.ViewUsersInGroupView.as_view(), name='view_users_in_group'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('user_list/', views.UserListView.as_view(), name='user_list'),


 ]


