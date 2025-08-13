from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Value(bool, num, str), Q=query, F=field
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Avg, Min, Max, Sum
from django.db.models import DecimalField
from django.db import transaction, connection
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem
from tags.models import TaggedItem
# pylint: disable=no-member


# @transaction.atomic()  # all code runs inside transaction
def say_hello(request):
    # filter rows whose unit_price is >= 20
    query_set = Product.objects.filter(unit_price__gte=20)
    query_set = Product.objects.filter(unit_price__range=(20, 30))
    # Product has FK to Collection which has id=1
    query_set = Product.objects.filter(collection__id=1)
    # Product has FK to Collection, which has id=(1, 2, 3)
    query_set = Product.objects.filter(collection__id__range=(1, 2, 3))
    # filter products that contain(insens) 'coffee' in 'title'
    query_set = Product.objects.filter(title__icontains='coffee')
    # filter products that's last updated in 2021
    query_set = Product.objects.filter(last_update__year=2021)
    # filter products with empty 'description' column
    query_set = Product.objects.filter(description__isnull=True)
    # filter customers with .com accounts
    query_set = Customer.objects.filter(email__endswith='.com')
    # filter collections without 'featured_product_id'
    query_set = Collection.objects.filter(featured_product_id__isnull=True)
    # filter products with 'inventory' < 10
    query_set = Product.objects.filter(inventory__lt=10)
    # filter orders with 'customer_id'=1
    query_set = Order.objects.filter(customer_id=1)
    # filter orders with 'customer_id'=1
    query_set = Order.objects.filter(customer_id=1)
    # OrderItem has FK to Product
    # Product has FK to Collection, which has id=3
    query_set = OrderItem.objects.filter(product__collection__id=3)
    # Product with inventory < 10 and price < 20
    query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    query_set = Product.objects.filter(
        inventory__lt=10).filter(unit_price__lt=20)
    # Product with inventory < 10 OR price < 20
    query_set = Product.objects.filter(
        Q(inventory__lt=10) | Q(unit_price__lt=20))
    # Product: inventory = unit_price
    query_set = Product.objects.filter(inventory=F('unit_price'))
    # Product: inventory = id(collection)
    query_set = Product.objects.filter(inventory=F('collection__id'))
    # Product: sort by 'title' (ASC by default)
    query_set = Product.objects.order_by('title')
    # Product: sort by 'unit_price'(ASC), 'title'(DESC)
    query_set = Product.objects.order_by('unit_price', '-title')
    # Product: sort by 'unit_price'(DESC), 'title'(ASC)
    query_set = Product.objects.order_by('unit_price', '-title').reverse()
    # Product: earliest sorts(ASC) and returns 1st object
    query_set = Product.objects.earliest('unit_price')
    # Product: latest sorts(DESC) and returns 1st object
    query_set = Product.objects.latest('unit_price')
    # Product: get 2nd 5 objects (LIMIT=5, OFFSET=5)
    query_set = Product.objects.all()[5:10]
    # Product: get specific cols with .values()
    query_set = Product.objects.values('id', 'title')
    # Product: get related field with __
    query_set = Product.objects.values('id', 'title', 'collection__title')
    # Product: get specific cols as tuples
    query_set = Product.objects.values_list('id', 'title', 'collection__title')
    # Product: get ordered products
    ordered_ids = OrderItem.objects.values('product_id').distinct()
    query_set = Product.objects.filter(id__in=ordered_ids).order_by('title')
    # Product: get specific cols with 'only'
    query_set = Product.objects.only('id', 'title', 'collection__title')
        # Product: get all FK fields + all its fields
    query_set = Product.objects.select_related('collection').all()
    # select_related(1) - for OneToMany and ForeignKey
    # prefetch_related(n) - for ManyToMany and reverse ForeignKey
    # all is optional here, it fetches anyways all Product fields
    query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # get last 5 orders with customer, items (incl. product)
    # prefetch_related('targetClassName_set') - gets OrderItem
    # _set is because of OneToMany relationship
    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # aggregate the data: Count, Min
    result = Product.objects.filter(collection__id=6) \
        .aggregate(count=Count('id'), min_price=Min('unit_price'))
    # Count orders
    result = Order.objects.aggregate(orders=Count('id'))
    # Count Product=1 sold
    result = OrderItem.objects.filter(product__id=1)\
        .aggregate(units_sold=Sum('quantity'))
    # Count Customer=1 orders
    result = Order.objects.filter(customer__id=1) \
        .aggregate(customer1=Count('id'))
    # min, max & avg price of products in collection 3
    result = Product.objects.filter(collection__id=3) \
        .aggregate(min=Min('unit_price'), 
                    max=Max('unit_price'), 
                    avg=Avg('unit_price'))
    # add new col 'is_new' to Customer with 'True' values
    result = Customer.objects.annotate(is_new=Value(True))
    # add new col 'new_id' to Customer with 'id'+1 values
    result = Customer.objects.annotate(new_id=F('id') + 1)
    # add new col 'full_name' to Customer with 'CONCAT' Func
    result = Customer.objects.annotate(
        full_name=Func(F('first_name'), Value(' '),
                       F('last_name'), function='CONCAT')
    )
    # add new col 'full_name' to Customer with 'CONCAT' Func
    result = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name'))
    # Count orders adding new col 'orders_count' to Customer
    result = Customer.objects.annotate(
        orders_count=Count('order'))
    # create disc_price using ExpressionWrapper()
    # F() Field is taken in relation to Product
    discounted_price = ExpressionWrapper(
        F('unit_price') * 0.8, output_field=DecimalField()
    )
    result = Product.objects.annotate(
        discounted_price=discounted_price
    )
    # Customers with their last order ID
    # 'order__id' refers to IDs of all orders made by that customer
    result = Customer.objects.annotate(
        last_order_id=Max('order__id')
    )
    # Collections with count of their product
    result = Collection.objects.annotate(
        products_count=Count('product')
    )
    # Customers with more than 5 orders
    # .annotate() adds orders_count field to each customer with number of orders they have placed
    result = Customer.objects \
        .annotate(orders_count=Count('order')) \
        .filter(orders_count__gt=5)
    # Customers & total amount they’ve spent
    # F() Fields are taken in relation to Customer
    # (unit_price × quantity) gives total price for 1 product,
    # and SUM() gives sum of customer's all orders
    result = Customer.objects.annotate(
        expenditure=Sum(
            F('order__orderitem__unit_price') *
            F('order__orderitem__quantity')
        )
    )
    # Top 5 best-selling products & their total sales
    result = Product.objects \
        .annotate(
            total_sales=Sum(
                F('orderitem__unit_price') *
                F('orderitem__quantity'))) \
        .order_by('-total_sales')[:5]
    
    TaggedItem.objects.get_tags_for(Product, 1)
    # Django uses queryset cache after evaluating it 1st time
    query_set = Product.objects.all()
    list(query_set)  # here it's evaluating query_set and storing it in query_set cache
    # query_set[0]  # here it's reading from query_set cache

    # To insert into DB, create instance of model:
    collection = Collection()  # create instance of model
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    # collection.featured_product_id = 1  # also possible
    collection.save()
    # now we can access Collection attributes(id, title, ...)
    # collection.id

    # # we can also create data for Collection with .create()
    # Collection.objects.create(title='example', featured_product_id=1)  # this includes .save()
    # collection.id

    # To update DB, get existing table(Collection) object:
    # Collection(pk=1) tells Django this is an update
    collection = Collection(pk=1)  # fetch existing row
    collection.title = 'Games'  # update any field
    collection.featured_product = None
    collection.save()

    # The Update above updates all fields, setting '' for missing fields, this causes data loss
    # To update certain fields (without loss), get all values first before changing any field
    collection = Collection.objects.get(pk=11)
    collection.featured_product = Product(2)
    collection.save()

    # another way to update specified fields
    Collection.objects.filter(pk=11).update(featured_product=None)

    # To delete, just use .delete()
    # collection = Collection(pk=11)
    # collection.delete()  # this deletes row with id=11

    # Collection.objects.filter(id__gt=5).delete()  # delete rows with id > 5

    # Create a shopping cart with an item
    # cart = Cart()
    # cart.save()
    # # or with .create()
    # Cart.objects.create(cart=Cart())
    # item1  = CartItem()
    # item1.cart = cart
    # item1.product = Product(1)
    # item1.quantity = 1
    # item1.save()

    # Update the quantity of item in shopping cart
    # item1 = CartItem.objects.get(pk=2)
    # item1.quantity = 3
    # item1.save()
    # Update with .update()
    CartItem.objects.filter(product_id=1).update(quantity=2)

    # Delete a shopping cart with its items
    # cart = CartItem(pk=1)
    # cart.delete()
    # Delete with .filter() & .delete()
    # CartItem.objects.filter(pk=2).delete()

    # below part of code will run inside transaction
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()
    
        # To make raw SQL query, use objects(manager).raw('')
        result = Product.objects.raw('SELECT * FROM store_product')

        # create cursor object
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM store_order')  # we can pass any SQL statement here
        cursor.close()  # close() to release allocated resources

        # create cursor object using 'with' without needing to close
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM store_orderitem')  # we can pass any SQL statement here
            # use callproc() to exec stored procedures
            # cursor.callproc('get_customers', [1, 2, 'a'])
    
    # pk is replacement for primary key column(e.g. id=1)
    # product = Product.objects.filter(pk=0).first()  # ->: None
    # exists = Product.objects.filter(pk=0).exists()  # ->: False
    
    return render(request, 'hello.html', {'name': 'Shakhzod', 'result': list(result) })
