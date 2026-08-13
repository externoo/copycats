from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal

from copycat.utils import uuid7

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name