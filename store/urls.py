from django.urls import path
from . import views

# pass type & variable with <type:var>
urlpatterns = [
    # as_view() converts ProductList to function based view
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view(), name='collection-list'),
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]
