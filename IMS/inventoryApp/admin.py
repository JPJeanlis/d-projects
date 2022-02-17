from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import Supplier, Category, Product, ProductInstance, CountryOfOrigin

"""Minimal registration of Models.
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(ProductInstance)
admin.site.register(Category)
admin.site.register(CountryOfOrigin)
"""

admin.site.register(Category)
admin.site.register(CountryOfOrigin)


class ProductsInline(admin.TabularInline):
    """Defines format of inline product insertion (used in SupplierAdmin)"""
    model = Product


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Administration object for Supplier models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('name',
                    'start_date', 'start_date')
    fields = ['name', 'business_type', ('start_date')]
    inlines = [ProductsInline]


class ProductsInstanceInline(admin.TabularInline):
    """Defines format of inline product instance insertion (used in BookAdmin)"""
    model = ProductInstance


class ProductAdmin(admin.ModelAdmin):
    """Administration object for Product models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of product instances in product view (inlines)
    """
    list_display = ('itemName', 'supplier', 'expiry', 'quantity',
                    'unit_cost', 'prize', 'note', 'addDate', 'display_category')
    inlines = [ProductsInstanceInline]


admin.site.register(Product, ProductAdmin)


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    """Administration object for ProductInstance models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ('product', 'status', 'customer', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('name', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'customer')
        }),
    )
