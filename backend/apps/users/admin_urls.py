from django.urls import path
from . import admin_views

urlpatterns = [
    path('users/', admin_views.AdminUserListView.as_view(), name='admin-users'),
    path('users/<uuid:pk>/', admin_views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('users/<uuid:pk>/deactivate/', admin_views.AdminUserDeactivateView.as_view(), name='admin-user-deactivate'),
    path('users/<uuid:pk>/activate/', admin_views.AdminUserActivateView.as_view(), name='admin-user-activate'),
    path('users/<uuid:pk>/delete/', admin_views.AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('broadcast/', admin_views.BroadcastNotificationView.as_view(), name='admin-broadcast'),
] 