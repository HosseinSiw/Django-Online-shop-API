from django.contrib import admin
from .models import Product, Category, ProductImage


class ProductAdmin(admin.ModelAdmin):
    ordering = ("name", "is_active", "price",)
    list_filter = ('name', 'stock', 'price',)
    list_display = ('name', "stock", 'price', "slug")
    search_fields = ('name', "price",)
    
    fieldsets = (
        ("Product", {"fields": ("name", "price", "stock", "category")}),
    )
    add_fieldsets = (
        ("Product", {"fields": ("name", "price", 'stock', 'category', "slug")})
    )





admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)




