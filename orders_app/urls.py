from django.urls import path
from .views import PlaceOrderView, UserOrderListView, OrderDetailView, ApproveOrderView

urlpatterns = [
    path('', UserOrderListView.as_view(), name='order-list'),
    path('place/', PlaceOrderView.as_view(), name='place-order'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<uuid:pk>/approve/', ApproveOrderView.as_view(), name='approve-order'),
]