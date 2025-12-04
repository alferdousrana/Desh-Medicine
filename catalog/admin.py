# catalog/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage, DisplayedCategories


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active")
    search_fields = ("name", "generic_name", "brand_name", "slug")
    list_filter = ("category", "is_active", "prescription_required")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline]   # 👈 multiple image support


@admin.register(DisplayedCategories)
class DisplayedCategoriesAdmin(admin.ModelAdmin):
    list_display = ("category", "position")
    list_editable = ("position",)
    ordering = ("position",)
