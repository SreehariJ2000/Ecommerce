from django.shortcuts import render,redirect
from Ecom_app.models import *
from math  import ceil
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'index.html')

def purchase(request):
    
    allProds=[]
    catprod=Product.objects.values('category','id')
    cats={item['category'] for item in catprod}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nslides=n // 4 + ceil((n / 4)- (n//4))
        allProds.append([prod,range(1,nslides),nslides])
    
    return render(request, 'purchase.html',{'allProds':allProds})
    


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login and try again")
        return redirect('/Ecom_auth/login')
    

    if request.method=="POST":

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
         

        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True

        #payment integration
        id = Order.order_id
        oid=str(id)+"OneStopShopify"
      
        param_dict = {

            'MID': 'add ur merchant id',
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    
    return render(request,'checkout.html')