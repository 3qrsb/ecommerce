from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db import transaction, connection
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem


def say_hello(request):
    
    # queryset = Product.objects.all() #retrieving all items
    # product = Product.objects.get(pk=1) #get specific item
    # product = Product.objects.filter(pk=0).first() #if the queryset is empty the first() method return None
    # exists = Product.objects.filter(pk=0).exists() #return bool
    # queryset = Product.objects.filter(unit_price__gt=20) #greater than 20
    # queryset = Product.objects.filter(unit_price__range=(20, 30)) #in range of 20 and 30
    # queryset = Product.objects.filter(collection__id__range=(1, 2, 3))
    # queryset = Product.objects.filter(title__icontains='coffee') # case insensitive search 'i'
    # queryset = Product.objects.filter(title__startswith='c') # start
    # queryset = Product.objects.filter(title__endswith='e') # end
    # queryset = Product.objects.filter(last_update__year=2021) # date
    # queryset = Product.objects.filter(description__isnull=True) # checking for null
    
    # complex queries 
    # queryset = Product.objects.filter(inventory__lt=10,unit_price__lt=20) 
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20)) # ~ == not
    
    # reference fields using f objects
    # queryset = Product.objects.filter(inventory=F('unit_price'))
    # queryset = Product.objects.filter(inventory=F('collection__id'))
    
    # sorting data
    # queryset = Product.objects.order_by('unit_price', '-title').reverse()
    # queryset = Product.objects.filter(collection__id=1).order_by('unit_price')
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earlies('unit_price')
    # product = Product.objects.latest('unit_price')
    
    # limiting results
    # queryset = Product.objects.all()[:5]
    
    # selecting specific fields
    # queryset = Product.objects.values('id', 'title')
    # queryset = Product.objects.values('id', 'title', 'collection__title') # access related fields with underscore, return dictionary
    # queryset = Product.objects.values_list('id', 'title', 'collection__title') # returns tuple
    # queryset = OrderItem.objects.values('product__id').distinct() # for removing duplicates
    
    # SELECT PRODUCTS THAT HAVE BEEN ORDERED AND SORT THEM BY TITLE
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    
    # deferring fields
    # queryset = Product.objects.only('id', 'title') # returns instances of the product class
    # queryset = Product.objects.defer('description')
    
    # selecting related objects
    # select_related (1) other end of the relationship has one instance
    # prefetch_related (n) has many objects
    # queryset = Product.objects.select_related('collection__someOtherField').all()
    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()
    
    # last 5 orders with their customer and items(incl product)
    # queryset = Order.objects.select_related('customer').order_by('-placed_at')[:5]
    # preload the items of these orders
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by('-placed_at')[:5]
    # span the relationship by adding two underscores
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    
    # aggregating objects
    # result = Product.objects.aggregate(Count('id'))
    # change key word to 'count'
    # result = Product.objects.aggregate(count = Count('id'))
    # minimum price
    # result = Product.objects.aggregate(count = Count('id'), min_price=Min('unit_price'))
    # result = Product.objects.filter(collection__id=1).aggregate(count = Count('id'), min_price=Min('unit_price'))
    # return all orders
    # result = Order.objects.aggregate(Count('id'))
    # return units of product 1 sold
    # result = OrderItem.objects.filter(product__id=1).aggregate(units_sold=Sum('quantity'))
    # return orders customer 1 placed
    # result = Order.objects.filter(customer__id=1).aggregate(Count('id'))
    # min, max, avg price of product in collection 1
    # result = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), avg_price=Avg('unit_price'), max_price=Max('unit_price'))
    
    # annotating objects
    # queryset = Customer.objects.annotate(is_new=Value(True))
    # queryset = Customer.objects.annotate(new_id=F('id') + 1)

    # calling database
    # queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function = 'CONCAT'))
    # queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
    
    # grouping data
    # queryset = Customer.objects.annotate(orders_count=Count('order'))
    
    # expression wrapper
    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price = discounted_price
    # )
    # Customers with their last order ID
    # queryset = Customer.objects.annotate(last_order_id = Max('order__id'))
    # Collections and count of their products
    # queryset = Collection.objects.annotate(products_count = Count('product'))
    # Customers with more than 5 orders
    # queryset = Customer.objects.annotate(orders_count = Count('order').filter(orders_count__gt=5))
    # Customers and the total amount they’ve spent
    # queryset = Customer.objects.annotate(total_spent=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity')))
    # Top 5 best-selling products and their total sales 
    # queryset = Product.objects.annotate(total_sales = Sum(F('orderitem__unit_price') * F('orderitem__quantity'))).order_by('-total_sales')[:5]
    
    # querying generic relationships
    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type = content_type,
    #         object_id = 1
    # )
    
    # custom managers
    # TaggedItem.objects.get_tags_for(Product, 1)
    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type = content_type,
    #         object_id = 1
    # )
    
    # queryset cache
    # caching happens only if we evaluate the entire query set first
    # queryset = Product.objects.all()
    # list(queryset)
    # queryset[0]
    
    # creating objects, insert a record in the database
    # collection = Collection(title='Video Games')
    
    # collection = Collection()
    # collection.title = 'Video Games' 
    # collection.featured_product = Product(pk=1)
    # collection.save()
    # collection.id
    
    # key words are not updated
    # collection = Collection.objects.create(name='Video Games', featured_product_id=1)
    # collection.id
    
    # updating database
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()
    # by default title = ''
    # Collection.objects.filter(pk=11).update(featured_product=None)
    
    # deleting objects
    # collection = Collection(pk=11)
    # collection.delete()
    # queryset = Collection.objects.filter(id__gt=5).delete()
    
    # some exercises
    # creating a shopping cart with an item
    # cart = Cart()
    # cart.save()
    # item1 = CartItem()
    # item1.cart = cart
    # item1.product_id = 1
    # item1.quantity = 1
    # item1.save()
    # updating the quantity of an item
    # item1 = CartItem.objects.get(pk=1)
    # item1.quantity = 2
    # item1.save()
    # removing a cart, deleting a cart causes deletion of its items 
    # due to cascading in the relationship between car and its items
    # cart = cart(pk=1)
    # cart.delete()
    
    # transactions
    # with transaction.atomic():

    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # raw sql queries, used for complex orm queries
    # queryset = Product.objects.raw('SELECT * FROM store_product')
    # queryset = Product.objects.raw('SELECT id, title FROM store_product')
    # queryset = Product.objects.raw('SELECT id, title FROM store_product')
    # cursor = connection.cursor()
    # cursor.execute('INSERT')
    # cursor.close()
    
    # with connection.cursor() as cursor:
    #     cursor.execute()
    # with connection.cursor() as cursor:
    #     cursor.callproc('get_customers', [1, 2, 'a'])
    
    
    # return render(request, 'hello.html', { 'name': 'Yers', 'result': result})
    return render(request, 'hello.html', { 'name': 'Yers', 'result': list(queryset)})