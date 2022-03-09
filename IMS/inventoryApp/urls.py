from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers'),
    path('supplier/<int:pk>',
         views.SupplierDetailView.as_view(), name='supplier-detail'),
]


urlpatterns += [
    path('myproducts/', views.LoanedProductsByUserListView.as_view(),
         name='my-transactions'),
    path(r'sold/', views.LoanedProductsAllListView.as_view(),
         name='all-transactions'),  # Added for challenge
]


# Add URLConf for a user to sell a product.
urlpatterns += [
    path('product/<uuid:pk>/sell/', views.sell_product,
         name='sell_product'),
]

# Add URLConf to create, update, and delete suppliers
urlpatterns += [
    path('supplier/create/', views.SupplierCreate.as_view(), name='supplier-create'),
    path('supplier/<int:pk>/update/',
         views.SupplierUpdate.as_view(), name='supplier-update'),
    path('supplier/<int:pk>/delete/',
         views.SupplierDelete.as_view(), name='supplier-delete'),
]

# Add URLConf to create, update, and delete products
urlpatterns += [
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/update/',
         views.ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/',
         views.ProductDelete.as_view(), name='product-delete'),
]

urlpatterns += [
    path('page1', views.page1, name='pageI'),
    path('page2', views.page2, name='pageII'),
    path('page3', views.page3, name='pageIII'),
]
