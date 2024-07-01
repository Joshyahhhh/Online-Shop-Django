from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("failed/", views.PaymentFailedView.as_view(), name="failed"),
    path('api/checkout-session/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),

]