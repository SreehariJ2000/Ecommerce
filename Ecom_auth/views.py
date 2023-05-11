from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
#class based
from django.views.generic import View

#  for activate user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str

#getting tokens from utils
from .utils import *


# email
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings

from django.core.mail import EmailMessage

#threading
import threading

class EmailThread(threading.Thread):
       def __init__(self, email_message):
              super().__init__()
              self.email_message=email_message
       def run(self):
              self.email_message.send()

# Create your views here.
def signup(request):
    if request.method=="POST":
            email=request.POST['email']
            password=request.POST['pass1']
            confirm_password=request.POST['pass2']
            if password!=confirm_password:
                    messages.warning(request,"password is not matching")
                    return render(request,'auth/signup.html')
            try:
                      if User.objects.get(username=email):
                             messages.warning(request,"Email is already taken")
                             return render(request,'auth/signup.html')
            except Exception as identifiers:
                      pass

            user=User.objects.create_user(email,email,password)
            user.is_active=False  #make the user inactive
            user.save()
            current_site=get_current_site(request)   #get link of site
            email_subject="Activate your account"
            message=render_to_string('auth/activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link")



           
            return redirect('/Ecom_auth/login/')
                    
    return render(request,'auth/signup.html')
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('/Ecom_auth/login/')
        return render(request,"auth/activatefail.html")


def handlelogin(request):
     if request.method=="POST":
            username=request.POST['email']
            password=request.POST['pass1']
            myuser=authenticate(username=username,password=password)
            

            if myuser is not None:
                   login(request,myuser)
                   messages.success(request,"Login Sucess!!!")
                   return render(request,'index.html')
            else:
                   messages.error(request,"Some thing went wrong")
                   return redirect('/Ecom_auth/login')
     return render(request,'auth/login.html')

def handlelogout(request):
       logout(request)
       messages.success(request,"Logout success")
       return redirect('/Ecom_auth/login/')