from django.contrib import admin

from app import models


@admin.register(models.ProductWB)
class ProductWBAdmin(admin.ModelAdmin):
    list_display = [
        "id", "sku", "name", "price", "date_updated", "is_check"
    ]
    list_display_links = ["id", "sku", "name", "price"]
    search_fields = ["name", "sku"]
    list_filter = ("is_active",  "is_check")


@admin.register(models.Product1C)
class Product1CAdmin(admin.ModelAdmin):
    list_display = [
        "id", "sku", "price", "date_updated"
    ]
    list_display_links = ["sku", "price", "date_updated"]
    search_fields = ["sku"]
    

@admin.register(models.Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = [
        "id", "product", "name", "value"
    ]
    list_display_links = ["product", "name", "id"]
    search_fields = ["product", "name"]


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "id", "product", "username", "create_at"
    ]
    list_display_links = ["product", "username", "id"]
    search_fields = ["product", "username"]
    list_filter = ("create_at",)


admin.site.register(models.PriceHistory)
admin.site.register(models.Proxy)

