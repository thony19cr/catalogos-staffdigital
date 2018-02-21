from django.conf.urls import url, include
from productos.views import (
    ProductAllView, GetProductoView, CreateProductoView,
    UpdateProductoView,  DeleteProductoView, SearchOnProducts, HomeView,
    ProductBuyView, QuerySearchView
)

urlpatterns = [
    url(r"products/$", ProductAllView.as_view(), name="obtener_todos_productos"),
    url(r'create-product/$', CreateProductoView.as_view(), name='crear_producto'),
    url(r'get-product/(?P<id>\d+)/$', GetProductoView.as_view(), name='obtener_producto'),
    url(r'put-product/(?P<id>\d+)/$', UpdateProductoView.as_view(), name='actualizar_producto'),
    url(r'delete-product/(?P<id>\d+)/$', DeleteProductoView.as_view(), name='actualizar_producto'),
    url(r'search-products/$', SearchOnProducts.as_view(), name='buscar_productos'),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r"product/(?P<pk>\d+)/buy/$", ProductBuyView.as_view(), name="buy"),
    url(r'pagination-products/(?P<page>\d+)/$', QuerySearchView.as_view(), name='paginar_productos'),
]
