from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('', ProductListView.as_view(), name='products'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
]