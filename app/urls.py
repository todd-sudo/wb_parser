from django.urls import path

from app.views import (
    RunParserBySkuListView,
    GetProductsPriceView,
    GetProductDetailView,
    GetProductsPriceBySkuList,
    GetProductsContentView,
    GetProductsContentBySkuList,
    GetUnderpriceProductsView,
    GetUnderpriceProductsToCsvView
)

urlpatterns = [
    path(
        "parser/get-underprice-products-to-csv/",
        GetUnderpriceProductsToCsvView.as_view(),
        name="get_underprice_products_to_csv"
    ),
    path(
        "parser/get-underprice-products/",
        GetUnderpriceProductsView.as_view(),
        name="get_underprice_products"
    ),
    path(
        "parser/run-parser-by-sku-list/",
        RunParserBySkuListView.as_view(),
        name="run_parser_by_sku_list"
    ),
    path(
        "get-product/<str:sku>/",
        GetProductDetailView.as_view(),
        name="get_detail_product"
    ),
    path(
        "get-products-price/",
        GetProductsPriceView.as_view(),
        name="get_products_price"
    ),
    path(
        "get-products-price-by-sku-list/",
        GetProductsPriceBySkuList.as_view(),
        name="get_products_price_by_sku_list"
    ),
    path(
        "get-products-content/",
        GetProductsContentView.as_view(),
        name="get_products_content"
    ),
    path(
        "get-products-content-by-sku-list/",
        GetProductsContentBySkuList.as_view(),
        name="get_products_content_by_sku_list"
    )
]
