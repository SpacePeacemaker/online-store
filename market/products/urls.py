from django.urls import path
from .views import ProductListView, ProductDetailView, ProductsViewsView, DiscountListView

app_name = "products"


urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("history", ProductsViewsView.as_view(), name="products-history"),
    path("discount/", DiscountListView.as_view(), name="discount-products"),
]
