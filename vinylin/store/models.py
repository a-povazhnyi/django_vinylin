from django.db import models


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


class Sale(models.Model):
    product = models.OneToOneField(
        to='Product',
        null=True,
        on_delete=models.SET_NULL,
    )
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    product = models.ForeignKey(
        to='Product',
        on_delete=models.CASCADE,
    )
    image = models.ImageField()

    def get_path_name(self):
        pass


class AbstractProduct(models.Model):
    title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    part_number = models.CharField(max_length=100, null=True)
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


class Storage(models.Model):
    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)

    @property
    def status(self):
        if self.quantity < 1:
            return 'out_of_stock'
        if self.quantity < 10:
            return 'running_low'
        return 'in_stock'
