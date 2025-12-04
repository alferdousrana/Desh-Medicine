# catalog/urls.py

from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, DisplayedCategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("home-categories", DisplayedCategoryViewSet, basename="home-category")

urlpatterns = router.urls
