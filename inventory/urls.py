from django.urls import path
from .views import (
    MainCategoryListView, MainCategoryCreateView, MainCategoryUpdateView, MainCategoryDeleteView,ProductManagerListView,
    SubCategoryListView, SubCategoryCreateView, SubCategoryUpdateView, SubCategoryDeleteView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
)
from .import views

app_name = 'inventory'

urlpatterns = [

    path('main-categories/', MainCategoryListView.as_view(), name='main_category_list'),
    path('main-categories/add/', MainCategoryCreateView.as_view(), name='main_category_add'),
    path('main-categories/<int:pk>/edit/', MainCategoryUpdateView.as_view(), name='main_category_edit'),
    path('main-categories/<int:pk>/delete/', MainCategoryDeleteView.as_view(), name='main_category_delete'),


    path('sub-categories/', SubCategoryListView.as_view(), name='sub_category_list'),
    path('sub-categories/add/', SubCategoryCreateView.as_view(), name='sub_category_add'),
    path('sub-categories/<int:pk>/edit/', SubCategoryUpdateView.as_view(), name='sub_category_edit'),
    path('sub-categories/<int:pk>/delete/', SubCategoryDeleteView.as_view(), name='sub_category_delete'),

#manager

    path('sub/manager/', views.SubCategoryManagerListView.as_view(), name='sub_list'),
    path('sub/manager/add/', views.SubCategoryManagerCreateView.as_view(), name='sub_add'),
    path('sub/manager/<int:pk>/edit/', views.SubCategoryManagerUpdateView.as_view(), name='sub_edit'),
    path('sub/manager/<int:pk>/delete/', views.SubCategoryManagerDeleteView.as_view(), name='sub_delete'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

#manager
    path('our/product', ProductManagerListView.as_view(), name='list_products'),

    path('', views.TaxCategoryListView.as_view(), name='taxcategory-list'),
    path('create/', views.TaxCategoryCreateView.as_view(), name='taxcategory-create'),
    path('<int:pk>/edit/', views.TaxCategoryUpdateView.as_view(), name='taxcategory-edit'),
    path('<int:pk>/delete/', views.TaxCategoryDeleteView.as_view(), name='taxcategory-delete'),
]
