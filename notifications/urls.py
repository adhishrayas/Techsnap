from django.urls import path
from .views import CreateNotificationView,GetAllNotificationView,GetReadNotificationsView,GetUnreadNotificationsView,SeeNotificationView

urlpatterns = [
    path('create_notif/',CreateNotificationView.as_view(),name = "Create Notification"),
    path('get_notifs/',GetAllNotificationView.as_view(),name = "Get all Notifications"),
    path('get_read_notifs/',GetReadNotificationsView.as_view(),name = "Get all Read Notifications"),
    path('get_unread_notifs/',GetUnreadNotificationsView.as_view(),name = "Get Unread Notifications"),
    path('get_notif_details/',SeeNotificationView.as_view(),name = "Details of Notification")
]
