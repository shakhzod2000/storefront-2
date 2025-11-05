from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse  # third party import
from . import models  # local import


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'  # comes after 'By' in filter section
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        # tuples represent filters, ('filter', 'name')
        return [
            ('<10', 'Low inventories')
        ]
    
    def queryset(self, request, queryset):
        # self.value() = parameter_name
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)



class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    autocomplete_fields = ['product']
    max_num = 1
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(
                f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''



# make ProductAdmin() an admin model for Product() class
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug']
    # exclude = ['promotions']
    # readonly_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    # load related object(collection) with list_select_related=['']
    list_select_related = ['collection']  # eager load collection
    search_fields = ['title']
    ordering = ['title']

    def collection_title(self, product):
        return product.collection.title

    # add sorting option to inventory_status with @admin.display()
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        # every ModelAdmin has message_user() method
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['store/styles.css'], # applied everywhere
            # 'screen': ['styles.css'], # applied to screens
            # 'print': ['styles.css'] # applied when printing a page
        }



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['first_name', 'last_name',
                    'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='count_order_annot')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'order__count': customer.count_order_annot
            })
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.count_order_annot)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            count_order_annot = Count('order')
        )

# OrderItemInline inherits from ModelAdmin
# admin.StackedInline also possible
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 5
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    list_per_page = 10
    search_fields = ['title']

    @admin.display(ordering='products_counter')
    def products_count(self, collection):
        # reverse formula: reverse('admin:app_target-model_target-page')
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_counter)
    
    # ModelAdmin has get_queryset() method
    # get_queryset() returns parent model of self
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_counter=Count('products')
        )

# admin.site.register(models.Customer, CustomerAdmin)
# below is another way to make ProductAdmin an admin model for Product class
# admin.site.register(models.Product, ProductAdmin)
