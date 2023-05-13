from django.shortcuts import render
from Ecom_app.models import *
from math  import ceil
# Create your views here.
def home(request):
    current_user=request.user
    print(current_user)
    allProds=[]
    catprod=Product.objects.values('category','id')
    cats={item['category'] for item in catprod}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nslides=n // 4 + ceil((n / 4)- (n//4))
        allProds.append([prod,range(1,nslides),nslides])
    
    return render(request, 'index.html',{'allProds':allProds})