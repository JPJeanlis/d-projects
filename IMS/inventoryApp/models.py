# Required to assign customers after a purchase
from django.contrib.auth.models import User
from datetime import date
import uuid  # Required for unique product instances
from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Category(models.Model):
    """Model representing a product category (Electronics, Style& Fashion, Sporting Goods, Pets Supplies, Other categories)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a product category (Electronics, Style& Fashion, Sporting Goods, Pets Supplies, Other categories)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class CountryOfOrigin(models.Model):
    """Model representing a CountryOfOrigin (China, Canada, USA, Mexico, Haiti)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the product's category (China, Canada, USA, Mexico, Haiti)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Product(models.Model):
    """Model representing a product (but not a specific copy of a product)."""
    itemName = models.CharField(max_length=200)
    expiry = models.CharField(max_length=30)
    quantity = models.FloatField()
    unit_cost = models.FloatField()
    prize = models.CharField(max_length=30)
    note = models.CharField(max_length=30)
    addDate = models.DateField()
    supplier = models.ForeignKey(
        'Supplier', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because a product can be bought from one supplier only, but suppliers can have multiple products

    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the product")
    sku = models.CharField('SKU', max_length=13,
                           unique=True,
                           help_text='13 Character<a href="https://www.shopify.ca/encyclopedia/stock-keeping-unit-sku">SKU number</a>')
    category = models.ManyToManyField(
        Category, help_text="Select a category for this product")
    # ManyToManyField used because a category can contain many products and a Product can cover many categories.
    # Category class has already been defined so we can specify the object above.
    countryoforigin = models.ForeignKey(
        'CountryOfOrigin', on_delete=models.SET_NULL, null=True)

    class Meta:
        # to sort by itemName, then by supplier
        ordering = ['itemName', 'supplier']

    def display_category(self):
        """Creates a string for the Category. This is required to display category in Admin."""
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'

    def get_absolute_url(self):
        """Returns the url to access a particular product instance."""
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.itemName


class ProductInstance(models.Model):
    """Model representing a specific product loan within the business)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular product across whole organization")
    product = models.ForeignKey(
        'Product', on_delete=models.RESTRICT, null=True)
    customer_full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=14)
    social_S_N = models.CharField(max_length=200)
    driver_license = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    due_payment_date = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_payment_date and date.today() > self.due_payment_date:
            if self.purchase_date and date.today() > self.purchase_date:
                return True
        return False

    LOAN_STATUS = (
        ('d', 'Paid'),
        ('o', 'Loan'),
        ('o', 'Due'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Product availability')

    class Meta:
        ordering = ['due_payment_date', 'purchase_date']
        permissions = (
            ("can_mark_returned", "Set product as damaged"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.product.itemName)


class Supplier(models.Model):
    """Model representing an supplier."""
    name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name', 'business_type']

    def get_absolute_url(self):
        """Returns the url to access a particular supplier instance."""
        return reverse('supplier-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.name, self.business_type)
