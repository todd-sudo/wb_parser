import datetime

from rest_framework import serializers

from app.models import (
    ProductWB, Specification, Feedback, Product1C, PriceHistory
)


class SpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specification
        exclude = ["product"]


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        exclude = ["product"]


class PriceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceHistory
        exclude = ["product_wb"]


class Product1CSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product1C
        fields = "__all__"


class ProductWBDetailSerializer(serializers.ModelSerializer):
    feedbacks_set = FeedbackSerializer(many=True, read_only=True, default=[])
    specifications_set = SpecificationSerializer(many=True, read_only=True, default=[])
    prices = PriceHistorySerializer(many=True, read_only=True, default=[])
    product_1c = Product1CSerializer(read_only=True)

    class Meta:
        model = ProductWB
        fields = "__all__"


class ProductWBDetailContentSerializer(serializers.ModelSerializer):
    feedbacks_set = FeedbackSerializer(many=True, read_only=True, default=[])
    specifications_set = SpecificationSerializer(many=True, read_only=True, default=[])
    # prices = PriceHistorySerializer(many=True, read_only=True, default=[])
    product_1c = Product1CSerializer(read_only=True)

    class Meta:
        model = ProductWB
        fields = "__all__"


class ProductWBUnderpriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductWB
        fields = [
            "sku", "name", "price", "percentage", "url", "date_updated",
            "count_in_stock", "is_active", "count_in_stock_old", "basic_sale",
            "client_sale", "price_no_sale", "basic_price"
        ]


class ProductWBPriceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductWB
        fields = "__all__"


class SkuListSerializer(serializers.Serializer):
    sku_list = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ["sku_list"]


class SetProduct1CSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=200)
    price = serializers.FloatField(default=0.0)
    is_check = serializers.BooleanField(default=True)

    class Meta:
        fields = ["sku", "price", "is_check"]


class RunParserSerializer(serializers.Serializer):
    products = serializers.ListField(child=SetProduct1CSerializer())

    class Meta:
        fields = ["products"]

