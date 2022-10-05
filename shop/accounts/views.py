import email
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from accounts.models import Account
from cartapp.models import Cart, CartItem
from cartapp.views import _cart_id

# Create your views here.


def signin(request):
    # if 'username' in request.session:
    #     return redirect()
    print('hghg')
    if request.method == 'POST':
        print('vbnmmmmmmm')
        email = request.POST.get('email')
        password = request.POST.get('password')    

        user = authenticate(email = email,password = password)

    #     if user is not None:
    #         request.session['username'] = email
    #         login(request,user)
    #         return render(request,'index.html')

    #         # return redirect()
    #     else:
    #         messages.success(request,'Enter correct details')
    #         return redirect(signin)
    # return render(request,'login-register.html')

        if user is not None:
            try:
                carts = Cart.objects.get(cart_id=_cart_id(request))
                carts_item = CartItem.objects.filter(cart = carts) 
                users_item = CartItem.objects.filter(user = user)

                for x in carts_item:#if multiple item in cart 
                    a=0
                    if users_item:
                            for y in users_item:#check each items in users_items 
                                if  x.product == y.product:#if product in both carts_items from sessions id and users  product from cart_item(models) matches
                                    y.quantity += x.quantity#product items quantity will be sum of .....
                                    x.delete()#delete the carts_item  
                                    y.save()
                                    a=1
                                    break
                                if a==0:# to add if different product to user cart 
                                    x.user=user
                                    x.save()
                    else:
                        x.user=user
                        x.save()

            except:
                pass    
            login(request, user)
            request.session["username"] = email
            return render(request,'index.html')

        else:
            messages.success(request, "Enter correct deatils")
            return redirect(signin)
    return render(request, "login-registerold.html")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def signup(request):
    print("aaaaaaaa")
    if request.method =='POST':      
        print("bbbbbb")  
        username = request.POST['username']   
        first_name = request.POST['first_name']                
        last_name = request.POST['last_name']                
        email = request.POST['email']                
        phone_number = request.POST['phone_number']                
        password1 = request.POST['password1']                             
        password2 = request.POST['password2']  
        if password1 ==password2:
            if username=="":
                messages.error(request,"username is empty")
                return render(request,'signup.html')              
            elif len(username)<2:
                messages.error(request,"username is too short")
                return render(request,'signup.html')  
            elif not username.isidentifier():
                messages.error(request,"username start must with alphabets")
                return render(request,'signup.html')                     
            elif Account.objects.filter(username = username):
                messages.error(request,"username exits")
                return render(request,'signup.html')
            elif email=="":
                messages.error(request,"email field is empty")
                return render(request,'signup.html')
            elif len(email)<2:
                messages.error(request,"email is too short")
                return render(request,'signup.html')

            elif Account.objects.filter(email=email):
                messages.error(request,"email already exist try another")
                return render(request,'signup.html')
                
        user1 =Account.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1,phone_number=phone_number)
        user1.save()
        messages.success(request,"Registered Successfully")

        return redirect(signin)
        # else:
        #     messages.success(request,"password does not match")
        #     return render(request,'login-register.html')
    else:
        return render(request,'signup.html') 
        
    # return render(request,'login-register.html') 
    
def signout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(signin)
                                
                            
                     