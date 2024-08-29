from django.urls import path
from django.views.decorators.cache import cache_page
from texnomart import views
# from texnomart.auth import auth_views

urlpatterns = [
    # category urls
    path('',views.ProductListView.as_view()),
    path('categories/', views.CategoryListApiView.as_view()),
    path('category/<slug:slug>/',views.CategoryAllProducts.as_view()),

    # !!! 'texnomart-uz/category/add-category' yozsam  CategoryAllProducts ga o'tib qolyapti. shuning uchun 'add/category' yozdim!!!

    path('category/add/category/',views.CreateCategoryView.as_view()),
    path('category/<slug:slug>/delete/',views.DeleteCategoryView.as_view()),
    path('category/<slug:slug>/edit/',views.UpdateCategoryView.as_view()),
    # products
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view()),
    path('product/<int:id>/edit/', views. PruductEditView.as_view()),
    path('product/<int:id>/delete/', views.ProductDeleteView.as_view()),
    # attributes
    path('attribute-key/', views.AttributeKeyView.as_view()),
    path('attribute-value/', views.AttributeValueView.as_view()),

    ]

