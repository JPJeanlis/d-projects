from .models import Supplier, Category, Product, ProductInstance, CountryOfOrigin
from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
admin.site.site_header = 'Inventory Management System (IMS)'


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
                    'start_date', 'end_date')
    fields = ['name', 'business_type', ('start_date'), ('end_date')]
    inlines = [ProductsInline]


class ProductsInstanceInline(admin.TabularInline):
    """Defines format of inline product instance insertion (used in ProductAdmin)"""
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
    list_display = ('product', 'status', 'employee',
                    'due_payment_date', 'purchase_date', 'id')
    list_filter = ('status', 'due_payment_date', 'purchase_date')

    fieldsets = (
        (None, {
            'fields': ('product', 'customer_full_name', 'address', 'phone', 'comment', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_payment_date', 'purchase_date', 'employee')
        }),
    )
