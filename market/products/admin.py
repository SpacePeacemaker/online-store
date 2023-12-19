from django.contrib import admin  # noqa F401

from .models import (
    Category,
    Product,
    Banner,
    Review,
    ProductImage,
    ProductDetail,
    Detail,
    ProductsViews,
    DiscountSet,
    DiscountProduct,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "is_active"
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "date_of_publication", "category_id"
    list_display_links = ("name",)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = "product", "image", "is_active"
    list_display_links = ("product",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "product", "text", "user", "created_at"
    list_display_links = "product", "text", "user"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "product", "image", "sort_image"


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = "product", "detail", "value"
    list_display_links = ("detail",)


@admin.register(ProductsViews)
class ProductsViewsAdmin(admin.ModelAdmin):
    list_display = "product", "user", "created_at"
    list_display_links = "product", "user"


@admin.register(DiscountSet)
class DiscountSetAdmin(admin.ModelAdmin):
    list_display = "pk", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)


@admin.register(DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = "pk", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)
