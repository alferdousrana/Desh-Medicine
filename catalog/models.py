# catalog/models.py

from django.db import models
from accounts.utils import generate_unique_slug


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    """
    Desh Medicine product (medicine) model.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    generic_name = models.CharField(max_length=200, blank=True, null=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)

    # HTML supported description
    description = models.TextField(
        blank=True,
        null=True,
        help_text="HTML allowed (e.g. <b>bold</b>, <i>italic</i>, <br> line breaks).",
    )
    dosage_info = models.CharField(max_length=255, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, default="pcs")

    prescription_required = models.BooleanField(default=False)

    # main/primary image (optional)
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["generic_name"]),
            models.Index(fields=["brand_name"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Product, self.name)
        super().save(*args, **kwargs)


# 🔹 MULTIPLE IMAGES PER PRODUCT
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"


# 🔹 HOME PAGE DISPLAY CATEGORY ORDER
class DisplayedCategories(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="displayed_categories",
    )
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]  # home page e ei order e show

    def __str__(self):
        return f"Position {self.position} - {self.category.name}"
