import csv

from django.http import HttpResponse
from django.conf import settings
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, pagination
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from app.models import ProductWB, PriceHistory
from app.serializers import (
    ProductWBPriceListSerializer,
    ProductWBDetailSerializer,
    SkuListSerializer,
    ProductWBUnderpriceSerializer,
    ProductWBDetailContentSerializer,
    RunParserSerializer
)
from app.tasks import get_price_products_task


MAX_LEN_SKU_LIST_PRICE = 100
MAX_LEN_SKU_LIST_CONTENT = 50


class CustomPaginationPrice(pagination.PageNumberPagination):
    """ Кастомный класс пагинации для цен
    """
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


class CustomPaginationContent(pagination.PageNumberPagination):
    """ Кастомный класс пагинации для контента
    """
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 50


class RunParserBySkuListView(APIView):
    """ Запускает таску на парсинг по sku кодам
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RunParserSerializer,
        description="""
    Параметры:

    products - список товаров (sku - price)

    Example:

    {
        "products": [
            {
                "sku": 6583968,
                "price": 555,
                "is_check": true
            },
            {
                "sku": 7689878,
                "price": 247,
                "is_check": true
            },
            {
                "sku": 7546165,
                "price": 1573,
                "is_check": true
            }
        ]
    }
    """
    )
    def post(self, request: Request):
        data: dict = request.data

        products = data.get("products")
        print(products)
        get_price_products_task.apply_async((), {"products": products})

        return Response(data={"msg": "ok"}, status=status.HTTP_200_OK)


class GetProductDetailView(RetrieveAPIView):
    """ Получение товара по sku коду
    """
    permission_classes = (AllowAny,)
    queryset = ProductWB.objects.all()
    serializer_class = ProductWBDetailSerializer
    pagination_class = CustomPaginationContent
    lookup_field = "sku"

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "limit_prices",
                OpenApiTypes.STR,
                description="Кол-во объектов истории цен "
                            "(от самой последней до limit_prices). "
                            "По умолчанию = 20",
                required=False,
                location="query"
            ),
            OpenApiParameter(
                "date",
                OpenApiTypes.STR,
                description="История цен за конкретную дату. "
                            "Формат даты: 2022-12-14",
                required=False,
                location="query"
            ),
            OpenApiParameter(
                "sku",
                OpenApiTypes.STR,
                description="SKU-код товара",
                required=True,
                location="path"
            ),
        ],
        description="""
Параметры:

limit_prices - Кол-во объектов истории цен
(от самой последней до limit_prices) По умолчанию = 20

date - История цен за конкретную дату (Формат даты: 2022-12-14)

Параметры можно использовать только РАЗДЕЛЬНО! Если параметр date не пустой,
то параметр limit_prices не учитывается в запросе
"""
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        sku = filter_kwargs.get("sku")

        limit_prices = self.request.query_params.get(
            "limit_prices", settings.RETRIEVE_LIMIT_PRICES
        )
        limit_prices = int(limit_prices)

        date = self.request.query_params.get("date")

        queryset = self.get_queryset()

        if not date:
            price_history_ids = [
                p.pk for p in PriceHistory.objects.filter(
                    product_wb__sku=sku
                )[:limit_prices]
            ]
        else:
            price_history_ids = [
                p.pk for p in PriceHistory.objects.filter(
                    create_at=date
                )[:limit_prices]
            ]
        queryset = queryset.select_related("product_1c").prefetch_related(
            Prefetch(
                "prices",
                PriceHistory.objects.filter(pk__in=price_history_ids)
            )
        )
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class GetProductsPriceView(ListAPIView):
    """ Получение цен на товары из БД
    """
    permission_classes = (AllowAny,)
    queryset = ProductWB.objects.all()
    pagination_class = CustomPaginationPrice
    serializer_class = ProductWBPriceListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetProductsPriceBySkuList(APIView):
    """ Получение товаров по списку sku кодов
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        request=SkuListSerializer,
        description="""
    Параметры:
    
    sku_list - список SKU кодов товаров
    
    Example:
    
    {
        "sku_list": [
            "6583968",
            "7689878",
            "7546165"
        ]
    }
    """
    )
    def post(self, request: Request):
        data: dict = request.data
        sku_list = data.get("sku_list")
        if not sku_list:
            return Response(
                data={"msg": "sku_list null"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(sku_list) > MAX_LEN_SKU_LIST_PRICE:
            return Response(
                data={"msg": f"max len sku_list = {MAX_LEN_SKU_LIST_PRICE}"}
            )

        queryset = ProductWB.objects.filter(sku__in=sku_list)
        data_res = []

        for item in queryset:
            obj = item.__dict__
            obj.pop("_state")
            data_res.append(obj)

        return Response({"data": data_res}, status=status.HTTP_200_OK)


class GetProductsContentView(ListAPIView):
    """ Получение контента на товары из БД
    """
    permission_classes = (AllowAny,)
    queryset = ProductWB.objects.all()
    pagination_class = CustomPaginationContent
    serializer_class = ProductWBDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetProductsContentBySkuList(CreateAPIView):
    """ Получение товаров по списку sku кодов
    """
    permission_classes = (AllowAny,)
    queryset = ProductWB.objects.prefetch_related("specs_set")\
        .prefetch_related("feedbacks_set")
    serializer_class = SkuListSerializer
    # pagination_class = CustomPaginationContent

    @extend_schema(
        request=SkuListSerializer,
        description="""
    Параметры:
    
    sku_list - список SKU кодов товаров
    
    Example:
    
    {
        "sku_list": [
            "6583968",
            "7689878",
            "7546165"
        ]
    }
    """
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_ser = serializer.data
        headers = self.get_success_headers(data_ser)
        sku_list = data_ser.get("sku_list")
        if not sku_list:
            return Response(
                data={"msg": "sku_list null"},
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers
            )

        if len(sku_list) > MAX_LEN_SKU_LIST_CONTENT:
            return Response(
                data={"msg": f"max len sku_list = {MAX_LEN_SKU_LIST_CONTENT}"},
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers
            )

        queryset = self.get_queryset().filter(sku__in=sku_list)

        data_res = ProductWBDetailContentSerializer(
            instance=queryset, many=True, read_only=True
        )
        return Response(
            {"data": data_res.data}, status=status.HTTP_200_OK, headers=headers
        )


class GetUnderpriceProductsView(ListAPIView):
    """ Получение товаров по заниженной цене
    """
    permission_classes = (AllowAny,)
    queryset = ProductWB.objects.all()
    pagination_class = CustomPaginationContent
    serializer_class = ProductWBUnderpriceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "sort",
                OpenApiTypes.STR,
                description="Сортировка товаров",
                required=True,
                location="query"
            ),
        ],
        description="""    
    Параметры:
    
    ?sort — выбор сортировки
    
    Виды сортировок:

    gt    — заниженная цена ВБ 5% (p > 5)
    gt_lt —  от -5% до 5% (p > -5 && p < 5)
    lt    — завышенная цена ВБ -5% (p < -5)

    Сортировки можно использовать только РАЗДЕЛЬНО!
    """
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request: Request, *args, **kwargs):
        """
        /gt    — заниженная цена ВБ 5% (p > 5)
        /gt_lt —  от -5% до 5% (p > -5 && p < 5)
        /lt    — завышенная цена ВБ -5% (p < -5)
        """

        sort = request.query_params.get("sort")
        if sort not in ["gt", "lt", "gt_lt"]:
            return Response({"msg": "param sort is not null"})

        queryset = self.filter_queryset(self.get_queryset())

        if sort == "gt":
            queryset = queryset.filter(
                percentage__gt=settings.PERCENTAGE_MAX
            )
        if sort == "lt":
            queryset = queryset.filter(
                percentage__lt=settings.PERCENTAGE_MIN
            )
        if sort == "gt_lt":
            queryset = queryset.filter(
                percentage__gt=settings.PERCENTAGE_MIN
            ).filter(
                percentage__lt=settings.PERCENTAGE_MAX
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetUnderpriceProductsToCsvView(APIView):
    """ Получение товаров по заниженной цене
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "sort",
                OpenApiTypes.STR,
                description="Сортировка товаров",
                required=False,
                location="query"
            ),
            OpenApiParameter(
                "filename",
                OpenApiTypes.STR,
                description="Имя файла",
                required=False,
                location="query"
            ),
        ],
        description="""    
    Параметры:
    
    ?sort — выбор сортировки
    
    &filename - имя файла (
        без .csv, по дефолту = underprice_wb + _sort_name (lt, gt, gt_lt)
    )
    
    Виды сортировок:

    gt    — заниженная цена ВБ 5% (p > 5)
    gt_lt —  от -5% до 5% (p > -5 && p < 5)
    lt    — завышенная цена ВБ -5% (p < -5)
    all   — весь каталог

    Сортировки можно использовать только РАЗДЕЛЬНО! По дефолту sort=all
    """
    )
    def get(self, request: Request, *args, **kwargs):
        sort = request.query_params.get("sort", "all")
        if sort not in ["gt", "lt", "gt_lt", "all"]:
            sort = "all"

        filename = request.query_params.get("filename", "underprice_wb")

        queryset = ProductWB.objects.select_related("product_1c")

        if sort == "gt":
            queryset = queryset.filter(
                percentage__gt=settings.PERCENTAGE_MAX
            )
        if sort == "lt":
            queryset = queryset.filter(
                percentage__lt=settings.PERCENTAGE_MIN
            )
        if sort == "gt_lt":
            queryset = queryset.filter(
                percentage__gt=settings.PERCENTAGE_MIN
            ).filter(
                percentage__lt=settings.PERCENTAGE_MAX
            )

        count = 0
        response = HttpResponse()
        response[
            'Content-Disposition'] = f'attachment; filename={filename}_{sort}.csv'
        writer = csv.writer(response)
        for i in queryset:
            product_1c_sku = i.product_1c.sku
            product_1c_price = i.product_1c.price
            product_1c_date_updated = i.product_1c.date_updated

            obj: dict = i.__dict__
            obj.pop("_state")
            obj.pop("product_1c_id")
            obj["product_1c_sku"] = product_1c_sku
            obj["product_1c_price"] = product_1c_price
            obj["product_1c_date_updated"] = product_1c_date_updated
            # obj.pop("id")

            if count == 0:
                header = obj.keys()
                writer.writerow(header)

            count += 1
            writer.writerow(obj.values())
        return response

