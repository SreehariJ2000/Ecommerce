from django.shortcuts import render,redirect
from Ecom_app.models import *
from math  import ceil
from django.contrib import messages
import razorpay
from django.conf import settings

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
        print("*************************************8")
        print("*************************************8")
        print("AMount to be paid  ",amount)
        print(type(amount))
        
       
        print("*print the jason item *8")
        
        print(items_json,"/n",)

        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        print("order id=",Order.order_id)
        update.save()
        thank = True
        
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

        
        payment = client.order.create({ "amount":amount*100, "currency": "INR",'payment_capture':'1'})
        print(" I need to print payment .id 11111111111111111111111111111111===   ")
        print(payment.id)
        
        
        

        #payment integration


    return render(request, 'checkout.html')

        
        