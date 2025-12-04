# catalog/serializers.py

from rest_framework import serializers
from .models import Category, Product, ProductImage, DisplayedCategories


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    # Category slug diye create/update
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )
    # multiple images read-only list (create via admin or separate endpoint)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "generic_name",
            "brand_name",
            "description",        # HTML text
            "dosage_info",
            "price",
            "stock",
            "unit",
            "prescription_required",
            "image",              # main image
            "images",             # extra images
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class DisplayedCategorySerializer(serializers.ModelSerializer):
    # home page er jonno category details o pathabo
    category = CategorySerializer()

    class Meta:
        model = DisplayedCategories
        fields = ["id", "position", "category"]
