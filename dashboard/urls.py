from django.urls import path
from .views import ManagerDashboardView, CashierDashboardView, StoreDashboardView, RoomsDashboardView, SuperDashboardView


app_name = 'dashboard'
urlpatterns = [
    path('manager_dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('client_dashboard/', CashierDashboardView.as_view(), name='cashier_dashboard'),
    path('store_dashboard/', StoreDashboardView.as_view(), name='store_dashboard'),
    path('rooms_dashboard/', RoomsDashboardView.as_view(), name='rooms_dashboard'),
    path('super_dashboard/', SuperDashboardView.as_view(), name='super_dashboard'),

]