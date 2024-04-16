from django.shortcuts import render
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
    queryset = Product.objects.filter(description__isnull=True) # checking for null 
    
    
    
    return render(request, 'hello.html', { 'name': 'Yers', 'products': list(queryset)})