from django.urls import path
from . import views
from .views import (
    CartView, AddToCartView, RemoveFromCartView, MenuCategoryCreateView, MenuCategoryListView, MenuCategoryDetailView,
    MenuCategoryUpdateView, MenuCategoryDeleteView,
    MenuItemProductListView, MenuItemProductDetailView, MenuItemProductUpdateView, MenuItemProductDeleteView,
    OrderDetailView, PendingOrdersView, CompletedOrdersView,
    UpdateCartItemView, ConfirmOrderView, CancelOrderView, MenuItemListView, MenuItemDetailView, MenuItemCreateView,
    MenuItemUpdateView, MenuItemDeleteView, MenuItemProductCreateView, MenuManagerListView, OrderCashierDetailView,
)

app_name = 'cart'
urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<int:menu_item_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/remove/<int:menu_item_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("cart/update/<int:menu_item_id>/", UpdateCartItemView.as_view(), name="update-cart-item"),
    path("cart/confirm/", ConfirmOrderView.as_view(), name="confirm-order"),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/<int:pk>/cashier/', OrderCashierDetailView.as_view(), name='order-det'),
    path("cart/cancel/", CancelOrderView.as_view(), name="cancel-order"),
    path('search/', views.search_menu_item, name='search-menu-item'),
    path('pending-orders/', PendingOrdersView.as_view(), name='pending-orders'),
    path('completed-orders/', CompletedOrdersView.as_view(), name='completed-orders'),
    path('delete/<int:pk>/', views.delete_pending_order, name='delete_pending_order'),
    path('deleted/', views.DeletedOrderListView.as_view(), name='deleted_orders'),
    path('daily-sales/', views.DailySalesView.as_view(), name='daily_sales'),
    path('deleted/order/', views.DeletedOrderCashierListView.as_view(), name='deleted_order'),




    path('menu/', MenuItemListView.as_view(), name='menuitem-list'),
    path('<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
    path('create/', MenuItemCreateView.as_view(), name='menuitem-create'),
    path('<int:pk>/edit/', MenuItemUpdateView.as_view(), name='menuitem-edit'),
    path('<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menuitem-delete'),
    path('our/list', MenuManagerListView.as_view(), name='list_menu'),


    path('menu-item-products/', MenuItemProductListView.as_view(), name='menu_item_product_list'),
    path('menu-item-products/create/', MenuItemProductCreateView.as_view(), name='menu_item_product_create'),
    path('menu-item-products/<int:pk>/', MenuItemProductDetailView.as_view(), name='menu_item_product_detail'),
    path('menu-item-products/<int:pk>/edit/', MenuItemProductUpdateView.as_view(), name='menu_item_product_edit'),
    path('menu-item-products/<int:pk>/delete/', MenuItemProductDeleteView.as_view(), name='menu_item_product_delete'),


    path('categories/', MenuCategoryListView.as_view(), name='menu_category_list'),
    path('categories/create/', MenuCategoryCreateView.as_view(), name='menu_category_create'),
    path('categories/<int:pk>/', MenuCategoryDetailView.as_view(), name='menu_category_detail'),
    path('categories/<int:pk>/edit/', MenuCategoryUpdateView.as_view(), name='menu_category_edit'),
    path('categories/<int:pk>/delete/', MenuCategoryDeleteView.as_view(), name='menu_category_delete'),

]