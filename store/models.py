# store/models.py
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from uuid import uuid4
from .validators import validate_file_size


# pylint: disable=no-member
# create tables(models) in DB
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # ↓ if parent(Collection) class defined before child(Product), use ''
    # related_name='+' tells Django not to create reverse relationship
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']  # sort Collection by 'id'


class Product(models.Model):
    title = models.CharField(max_length=255)
    # slug is uniquely identifying last part of URL
    slug = models.SlugField()
    # null=True only applies to DB, for browsers use blank=True too
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)  # auto_now - updates(overwrites) datetime on every Product update
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    # ↓ Django creates reverse relationship btwn Promotion & Product
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(
        upload_to='store/images',
        validators=[validate_file_size]
    )
    # image = models.FileField(
    #     upload_to='store/images', 
    #     validators=[
    #         FileExtensionValidator(
    #             allowed_extensions=['pdf']
    #         )
    #     ]
    # )


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    phone = models.CharField(max_length=255)
    # blank=True makes field not required, null=True accepts null vals in DB
    birth_date = models.DateField(blank=True, null=True)
    membership = models.CharField(
        max_length=1, 
        choices=MEMBERSHIP_CHOICES, 
        default=MEMBERSHIP_BRONZE
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(models.Model):
    PENDING_PAYMENT = 'P'
    COMPLETE_PAYMENT = 'C'
    FAILED_PAYMENT = 'F'

    PAYMENT_STATUSES = [
        (PENDING_PAYMENT, 'Pending'),
        (COMPLETE_PAYMENT, 'Complete'),
        (FAILED_PAYMENT, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True) # auto_now_add - adds datetime for each product update(doesn't overwrite)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUSES, default=PENDING_PAYMENT)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderItem(models.Model):
    # Django creates reverse relationship with Order & Product classes
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    # prevent negative values with `PositiveSmallIntegerField()`
    # max of PositiveSmallIntegerField = 32767, 16-b int (2^15 - 1)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10, default='')
    # below is one to many relationship between two models
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    # we set `Customer` as a parent class of `Address`
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    # if product deleted, it should be removed from all CartItems
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
