# store/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from . import views
# from pprint import pprint  # pprint(pretty print)


# basename = prefix for 'name=' of views: -list, -detail
router = routers.DefaultRouter()
router.register(
    'products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
# pprint(router.urls)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
# basename = prefix for generating name of routes
# basename is set if 'get_queryset' is overridden in view
products_router.register(
    'reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register(
    'images', views.ProductImageViewSet, basename='product-images')

carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')
carts_router.register(
    'items', views.CartItemViewSet, basename='cart-items')


# pass type & variable with <type:var>
urlpatterns = router.urls + products_router.urls + carts_router.urls
# urlpatterns = [
#     path(r'', include(router.urls)),
#     path(r'', include(products_router.urls))
    ## as_view() converts ProductList to function based view
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]
