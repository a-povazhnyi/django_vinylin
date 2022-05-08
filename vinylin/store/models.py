from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator


class Category(models.Model):
    title = models.CharField(max_length=177)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Discount(models.Model):
    product = models.OneToOneField(
        to='Product',
        on_delete=models.CASCADE,
        related_name='discount',
    )
    amount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class AbstractProduct(models.Model):
    title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    part_number = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
    )
    overview = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Product(AbstractProduct):
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
    )
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def price_with_discount(self):
        try:
            discount_amount = self.discount.get(product=self).amount
            discount_amount *= 0.01
        except ObjectDoesNotExist:
            return None
        return self.price * (1 - discount_amount)


@receiver(post_save, sender=Product)
def create_storage_obj(sender, instance, created, **kwargs):
    """Creates Storage object after product creation"""
    if created:
        Storage.objects.create(product=instance)


class Storage(models.Model):
    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
        related_name='storage',
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return self.product.title

    @property
    def bad_status(self):
        if self.quantity < 1:
            return 'out_of_stock'
        if self.quantity < 10:
            return 'running_low'
        return False
