# accounts/utils.py

import random
import string
from django.utils.text import slugify


def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_unique_slug(model, field_value, slug_field_name='slug'):
    """
    Generate unique slug for given model+field.
    """
    base_slug = slugify(field_value) or generate_random_string(6)
    slug = base_slug

    while model.objects.filter(**{slug_field_name: slug}).exists():
        slug = f"{base_slug}-{generate_random_string(4)}"

    return slug
