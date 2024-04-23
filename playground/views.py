from django.shortcuts import render
from django.db.models import Q, F, Value
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer



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

    
    
    # return render(request, 'hello.html', { 'name': 'Yers', 'result': result})
    return render(request, 'hello.html', { 'name': 'Yers', 'result': list(queryset)})