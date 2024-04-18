from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product



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
    return render(request, 'hello.html', { 'name': 'Yers', 'products': list(queryset)})