from django.urls import path
from myapp.views import (
    index,
    add_item,
    update_item,
    delete_item,
    ProductListView,
    ProductDetailView,
    ProductDeleteView,
    contact,
    ProductViewSet
)
from api import views
from django.conf.urls import include
from rest_framework import routers

app_name = "myapp"

router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'orders', views.OrderDetailViewSet)

urlpatterns = [
    path("", index, name='index'),
    path("", ProductListView.as_view(), name="index"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("additem/", add_item, name="add_item"),
    path("updateitem/<int:my_id>/", update_item, name="update_item"),
    path("deleteitem/<int:pk>/", ProductDeleteView.as_view(), name="delete_item"),
    path('contact/', contact, name="contact"),
    path('productsapi/', ProductViewSet.as_view({'get': 'list'}), name='ProductViewSet'),
    path('api/', include(router.urls)),
]