# catalog/views.py

from rest_framework import viewsets, permissions
from .models import Category, Product, DisplayedCategories
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    DisplayedCategorySerializer,
)
from accounts.constants import ROLE_STAFF


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    SAFE methods (GET, HEAD, OPTIONS) sobar jonno open.
    Write methods (POST, PUT, PATCH, DELETE) sudhu staff role user der jonno.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        return (
            user.is_authenticated
            and getattr(user, "role", None) == ROLE_STAFF
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """
    /api/catalog/categories/
    /api/catalog/categories/<slug>/
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"  # slug diye retrieve/update/delete

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class ProductViewSet(viewsets.ModelViewSet):
    """
    /api/catalog/products/
    /api/catalog/products/<slug>/
    Filters:
      ?search=para
      ?category=pain-relief
      ?min_price=10&max_price=100
    """
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request

        search = request.query_params.get("search")
        category_slug = request.query_params.get("category")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if search:
            qs = qs.filter(name__icontains=search)
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        return qs


class DisplayedCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Home page e kon category gulo dekhabo + order.
    /api/catalog/home-categories/
    """
    queryset = DisplayedCategories.objects.select_related("category")
    serializer_class = DisplayedCategorySerializer
    permission_classes = [permissions.AllowAny]
