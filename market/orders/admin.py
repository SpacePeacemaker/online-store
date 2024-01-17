from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "phone_number",
        "created_at",
        "delivery_type",
        "address",
        "city",
        "payment_type",
        "status",
    ]
    list_filter = ["created_at"]
    inlines = [OrderItemInline]