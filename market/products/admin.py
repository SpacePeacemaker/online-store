from django.contrib import admin  # noqa F401

from .models import Product, Banner


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "date_of_publication", "category_id"
    list_display_links = ("name",)


class DetailsInline(admin.TabularInline):
    model = Product.details.through


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = "product", "image", "is_active"
    list_display_links = ("product",)
