
from accounts.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from product.models import Categoryies, Product,Productoffer,Categoryoffer
from shop import settings
from twilio.rest import Client
from cartapp.models import CartItem, coupon
from order.models import Order, OrderProduct
from django.shortcuts import render, redirect
import random
from product.models import *
# Create your views here.


def index(request):
    values = Categoryies.objects.all()
    allproduct = Product.objects.all()
    product     = Product.objects.all().filter(Is_available=True)
    # looping through all products to calculate its discount Price
    # for x in allproduct:
    #     list = []
        # ------------------------ checking for category offer ----------------------- #
        # try:
        #     category_offer = Categoryoffer.objects.get(
        #         category=x.category, is_active=True)
        #     list.append(category_offer.discount)
        # except ObjectDoesNotExist:
        #     print('no categoryOffer')
        #     pass

        # ------------------------ checking for Product offer ----------------------- #
        # try:
        #     product_offer = Productoffer.objects.get(
        #         product=x.id, is_active=True)
        #     list.append(product_offer.discount)
        # except ObjectDoesNotExist:
        #     print('no productOffer')
        #     pass
        # x.discount_price = 0
        # x.discount_price = None
        # if list:
        #     x.save()
        # else:
            # pass
    for m in product:
        try:
            Pro=Productoffer.objects.get(product__id=m.id)
            Prod=Pro.discount
            print(Prod, "Producvt discount percentage --------------------------------------------")
            if Pro :
                m.discount_price = int(m.price - (m.price*(Prod/100)))
                print('kkkkk',m.discount_price)
                m.save()
        except:
            m.discount_price = 0
            m.save()
    context = {
            "values": values,
            'product':product
        }
    return render(request, 'index.html', context )

#-----------------------------------------mobile-------------------------------------------------#
def otpmobile(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number == "":
            messages.info(request, 'Invalid Mobile number')
            return redirect(otpmobile)

        phone_no = "+91" + phone_number

        if Account.objects.filter(phone_number=phone_number).exists():
            user = Account.objects.get(phone_number=phone_number)
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)
            verification = client.verify \
                .services(settings.SERVICES) \
                .verifications \
                .create(to=phone_no, channel='sms')
            return render(request, 'otpnew.html', {'phone_number': phone_number})

        else:
            messages.info(request, 'Invalid Mobile number')
            return redirect(otpmobile)

    return render(request, "otpmobile.html")

# -----------------------------------------otp-----------------------------------------------#

def otp_login(request, phone_number):
    if request.method == 'POST':
        if Account.objects.filter(phone_number=phone_number):
            user = Account.objects.get(phone_number=phone_number)
            phone_no = "+91" + str(phone_number)
            otp_input = request.POST.get('otp')

            if len(otp_input) > 0:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)

                verification_check = client.verify \
                    .services(settings.SERVICES) \
                    .verification_checks \
                    .create(to=phone_no, code=otp_input)

                if verification_check.status == "approved":
                    # auth.login(request,user)
                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')
                    return redirect(index)
                else:
                    messages.error(request, 'Invalid OTP')
                    return render(request, 'otpnew.html', {'phone_number': phone_number})

            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'otpnew.html', {'phone_number': phone_number})

        else:

            messages.error(request, 'Invalid Phone number')
            return redirect(otp_login)
    return render(request, "otpnew.html")


# -------------------------------------------------------singleproduct-----------------------------------------#
def singleproduct(request, id):
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    values = Product.objects.get(id=id)
    print(values)
    return render(request, 'single-product.html', {"value": values})


# ----------------------------------------------------menproducts--------------------------------------------------#
def menproduct(request):
    Cat = Categoryies.objects.get(id=1)
    brand=Brands.objects.all()
    co=0
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat)
    brand=Brands.objects.all()
    for m in menproduct:
        try:

            Pro=Productoffer.objects.get(product__id=m.id)
            Prod=Pro.discount
            print(Prod, "Producvt discount percentage --------------------------------------------")
            if Pro :
                m.discount_price = int(m.price - (m.price*(Prod/100)))
                print('kkkkk',m.discount_price)
                m.save()
            try:
                if Catoffer:
                    m.discount_price = int(m.price - (m.price*(co/100)))
                    m.save()
            except:
                print('lllllll')        
                
                

        except:
            m.discount_price = None 
            m.save()
            try:
                if Catoffer:
                        print('hhhhhhhh',m.product_name)
                        m.discount_price = int(m.price - (m.price*(co/100)))
                        print('ttttttttt',m.discount_price)
                        m.save()
            except:
                m.discount_price = None
                m.save()
        try:
            if Pro and Catoffer:
                if Prod > co :
                    m.discount_price = int(m.price - (m.price*(Prod/100)))
                    m.save()
                else:
                    m.discount_price = int(m.price - (m.price*(co/100)))
                    m.save()
        except:
            # if Pro and Catoffer==None:
            #     w.discount_price = None
            #     w.save()
            print('iiiiiiiiiiiiiiiiiiii')
        try:
           
            print(Prod)
            print(Catoffer)
            if not Prod and Catoffer:
                print("ccccccccccc")
                m.discount_price = None
                m.save() 
        except:
            print("vvvvvvvvv")        
            # w.discount_price = None
            # w.save() 

    context ={
             'menproduct' : menproduct,
             'brand' : brand,
             'PercentDiscountProduct': Prod,
             'PercentDiscountCategory': co,


        }    
    return render(request, 'menpage.html', context)

# -----------------------------------------------------women products-----------------------------------------------#

def womenproduct(request):
    Cat = Categoryies.objects.get(id=2)
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    womenproduct = Product.objects.filter(category=Cat)
    for w in womenproduct:
        try:

            Pro=Productoffer.objects.get(product__id=w.id)
            Prod=Pro.discount
            if Pro :
                w.discount_price = int(w.price - (w.price*(Prod/100)))
                print('kkkkk',w.discount_price)
                w.save()
            try:
                if Catoffer:
                    w.discount_price = int(w.price - (w.price*(co/100)))
                    w.save()
            except:
                print('lllllll')        
                
                

        except:
            w.discount_price = None 
            w.save()
            try:
                if Catoffer:
                        print('hhhhhhhh',w.product_name)
                        w.discount_price = int(w.price - (w.price*(co/100)))
                        print('ttttttttt',w.discount_price)
                        w.save()
            except:
                w.discount_price = None
                w.save()
        try:
            if Pro and Catoffer:
                if Prod > co :
                    w.discount_price = int(w.price - (w.price*(Prod/100)))
                    w.save()
                else:
                    w.discount_price = int(w.price - (w.price*(co/100)))
                    w.save()
        except:
            # if Pro and Catoffer==None:
            #     w.discount_price = None
            #     w.save()
            print('iiiiiiiiiiiiiiiiiiii')
        try:
           
            print(Prod)
            print(Catoffer)
            if not Prod and Catoffer:
                print("ccccccccccc")
                w.discount_price = None
                w.save() 
        except:
            print("vvvvvvvvv")        
            # w.discount_price = None
            # w.save() 

    context ={
            'womenproduct' : womenproduct,
            'PercentDiscountProduct': Prod,
    }    
    return render(request, 'womenpage.html', context)
    # return render(request, 'womenpage.html', {'womenproduct': womenproduct})

#-------------------------------------------------------kidsproducts---------------------------------------------#
def kidsproduct(request):
    Cat = Categoryies.objects.get(id=3)
    Prod=0
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    kidsproduct = Product.objects.filter(category=Cat)
    for k in kidsproduct:
        try:

            Pro=Productoffer.objects.get(product__id=k.id)
            Prod=Pro.discount
            if Pro :
                k.discount_price = int(k.price - (k.price*(Prod/100)))
                print('kkkkk',k.discount_price)
                k.save()
            try:
                if Catoffer:
                    k.discount_price = int(k.price - (k.price*(co/100)))
                    k.save()
            except:
                print('lllllll')        
                
                

        except:
            k.discount_price = None 
            k.save()
            try:
                if Catoffer:
                        print('hhhhhhhh',k.product_name)
                        k.discount_price = int(k.price - (k.price*(co/100)))
                        print('ttttttttt',k.discount_price)
                        k.save()
            except:
                k.discount_price = None
                k.save()
        try:
            if Pro and Catoffer:
                if Prod > co :
                    k.discount_price = int(k.price - (k.price*(Prod/100)))
                    k.save()
                else:
                    k.discount_price = int(k.price - (k.price*(co/100)))
                    k.save()
        except:
            # if Pro and Catoffer==None:
            #     w.discount_price = None
            #     w.save()
            print('iiiiiiiiiiiiiiiiiiii')
        try:
           
            print(Prod)
            print(Catoffer)
            if not Prod and Catoffer:
                print("ccccccccccc")
                k.discount_price = None
                k.save() 
        except:
            print("vvvvvvvvv")        
            # w.discount_price = None
            # w.save() 

        context ={
        'kidsproduct' : kidsproduct,
        'PercentDiscountProduct': Prod,
}    
    return render(request, 'kidspage.html', context)
    return render(request, 'kidspage.html', {'kidsproduct': kidsproduct})


# -----------------------------------------------------checkout-------------------------------------#

def checkout(request, total=0, quantity=0, cart_items=None, tax=0, grand_total=0):

    if "coupon_code" in request.session:
        coupons = coupon.objects.get(
            coupon_code=request.session["coupon_code"])
        reduction = coupons.discount_percentage
    else:
        reduction = 0

    if request.user.is_authenticated:
        rawtotal = 0
        address = Address.objects.filter(user=request.user)[0:2]
        try:

            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
            for cart_item in cart_items:
                if cart_item.product.discount_price is not None:
                    total += (cart_item.product.discount_price *
                              cart_item.quantity)
                    quantity += cart_item.quantity
                else:
                    total += (cart_item.product.price*cart_item.quantity)
                    quantity += cart_item.quantity
                rawtotal += (cart_item.product.price*cart_item.quantity)

            tax = (2*total)/100
            grand_total = total + tax-reduction*total/100
            coupon_discount=reduction*total/100

        except ObjectDoesNotExist:
            pass  # just ignore

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
            'address': address,
            'coupon_discount': coupon_discount
        }
        return render(request, 'checkout.html', context)

    else:
        return redirect(index)

# -----------------------------------------------------address add------------------------------------------#


def addaddress(request):

    if request.method == 'POST':
        user = request.user
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone_number = request.POST['phone_number']
        Email_Address = request.POST['Email_Address']
        address = request.POST['Address']
        Town = request.POST['Town']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if firstname == "":
            messages.error(request, "NameField is empty")
            return render(request, "addaddress.html")

        elif len(firstname) < 2:
            messages.error(request, "Name is too short")
            return render(request, "addaddress.html")

        elif not firstname.isalpha():
            messages.error(request, "Name must contain alphabets")
            return render(request, "addaddress.html")

        elif not firstname.isidentifier():
            messages.error(request, "name start must start with alphabets")
            return render(request, "addaddress.html")

        elif Email_Address == "":
            messages.error(request, "email field is empty")
            return render(request, "addaddress.html")

        elif len(Email_Address) < 2:
            messages.error(request, "email is too short")
            return render(request, "addaddress.html")

        elif len(phone_number) < 10:
            messages.error(request, "Mobile Number should be 10 Digits")
            return render(request, "addaddress.html")

        elif Address.objects.filter(Email_Address=Email_Address):
            messages.error(request, "email already exist try another")
            return render(request, "addaddress.html")

        else:
            address = Address(user=user,
                              firstname=firstname,
                              lastname=lastname,
                              phone_number=phone_number,
                              Email_Address=Email_Address,
                              Addressfield=address,
                              Town=Town,
                              state=state,
                              pincode=pincode)

            address.save()
            return redirect(checkout)
    return render(request, 'addaddress.html')


# -----------------------------------------------------address delete-------------------------------------#


def addressdelete(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect(userprofile)

# -----------------------------------------------------edit address-------------------------------------#


def editaddress(request, id):
    address = Address.objects.get(id=id)
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone_number = request.POST.get('phone_number')
        Email_Address = request.POST.get('Email_Address')
        address = request.POST.get('address')
        Town = request.POST.get('Town')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        address.firstname = firstname
        address.lastname = lastname
        address.phone_number = phone_number
        address.Email_Address = Email_Address
        address.address = address
        address.Town = Town
        address.state = state
        address.pincode = pincode
        address.save()

        return redirect(userprofile)

    return render(request, "editaddress.html", {'address': address})


# -----------------------------------------------------men search-------------------------------------#

def mensearch(request):
    theproduct = None
    searchvalue = None
    if request.method == 'POST':
        searchvalue = request.POST.get('search')
        print(searchvalue)
        try:
            menproduct = Product.objects.filter(
                product_name__icontains=searchvalue)
            print(theproduct)

            return render(request, 'menpage.html', {'menproduct': menproduct})
        except:
            return render(request, 'Searchnotfound.html')

# -----------------------------------------------------women search-------------------------------------#


def womensearch(request):
    theproduct = None
    searchvalue = None
    if request.method == 'POST':
        searchvalue = request.POST.get('search')
        print(searchvalue)
        try:
            womenproduct = Product.objects.filter(
                product_name__icontains=searchvalue)
            print(theproduct)

            return render(request, 'womenpage.html', {'womenproduct': womenproduct})
        except:
            return render(request, 'Searchnotfound.html')


# -----------------------------------------------------kids search-----------------------------------------#

def kidsearch(request):
    theproduct = None
    searchvalue = None
    if request.method == 'POST':
        searchvalue = request.POST.get('search')
        print(searchvalue)
        try:
            kidsproduct = Product.objects.filter(
                product_name__icontains=searchvalue)
            print(theproduct)

            return render(request, 'kidspage.html', {'kidsproduct': kidsproduct})
        except:
            return render(request, 'Searchnotfound.html')



# -----------------------------------------------------user profile-------------------------------------#

def userprofile(request):
    acc = Account.objects.get(email=request.user)
    print(acc)
    addresses = Address.objects.filter(user=request.user)
    print(addresses)
    context = {
        'acc': acc,
        'addresses': addresses
    }
    return render(request, 'userprofile.html', context)


# ----------------------------------------------------profile address-------------------------------------#


def useraddress(request):

    if request.method == 'POST':
        user = request.user
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        print('address')
        phone_number = request.POST['phone_number']
        print('name')
        Email_Address = request.POST['Email_Address']
        address = request.POST['Address']
        Town = request.POST['Town']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if firstname == "":
            messages.error(request, "NameField is empty")
            return render(request, "userprofileaddress.html")

        elif len(firstname) < 2:
            messages.error(request, "Name is too short")
            return render(request, "userprofileaddress.html")

        elif not firstname.isalpha():
            messages.error(request, "Name must contain alphabets")
            return render(request, "userprofileaddress.html")

        elif not firstname.isidentifier():
            messages.error(request, "name start must start with alphabets")
            return render(request, "userprofileaddress.html")

        elif Email_Address == "":
            messages.error(request, "email field is empty")
            return render(request, "userprofileaddress.html")

        elif len(Email_Address) < 2:
            messages.error(request, "email is too short")
            return render(request, "userprofileaddress.html")

        elif len(phone_number) < 10:
            messages.error(request, "Mobile Number should be 10 Digits")
            return render(request, "userprofileaddress.html")

        elif Address.objects.filter(Email_Address=Email_Address):
            messages.error(request, "email already exist try another")
            return render(request, "userprofileaddress.html")

        else:
            address = Address.objects.create(user=user,
                                             firstname=firstname,
                                             lastname=lastname,
                                             phone_number=phone_number,
                                             Email_Address=Email_Address,
                                             Addressfield=address,
                                             Town=Town,
                                             state=state,
                                             pincode=pincode)

            address.save()
            return redirect(userprofile)

    return render(request, 'userprofileaddress.html')


# -----------------------------------------------------user order details-------------------------------------#


def userorder(request):
    orders = OrderProduct.objects.filter(user=request.user)
    print(orders)
    return render(request, 'userorder.html', {'orders': orders})

# -----------------------------------------------------cancel order-------------------------------------#


def cancelorder(request, id):
    orders = OrderProduct.objects.get(id=id)
    orders.status = 'Cancelled'
    orders.save()
    return redirect(userorder)


def order_cancel(request, id):
    user = request.user
    if request.user.is_authenticated:
        orders = Order.objects.get(id=id)
        orders.status = "cancelled"
        orders.save()
        orderproduct = OrderProduct.objects.filter(order=orders)
        orderproduct.product_status = "cancelled"
        orderproduct.save()
        if orders.payment.payment_method == "cashondelivery":
            pass
        else:
            pass

        for x in orderproduct:
            product = product.objects.get(id=x.product.id)
            product.stock += x.quantity
            product.save()

    return redirect(userprofile)


def product_order_cancel(request, id):
    users = request.user
    print("ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.get(id=id)
        orderproduct.status = "cancelled"
        orderproduct.save()

        producte = Product.objects.get(id=orderproduct.product.id)
        producte.stock += orderproduct.quantity
        producte.save()
    return redirect(userorder)


def product_return(request, id):
    if request.user.is_authenticated:
        

        # orders=order.objects.get(id=id)
        order_products = OrderProduct.objects.get(id=id)
        # order_date=order_products.order.date
        # order_products =order_product(product_status="return_accepted")
        order_products.status = "Returned"

        order_products.save()
        # orders=order(status="return_accepted")
        # orders.save()
        # for x in order_products:
        product = Product.objects.get(id=order_products.product.id)
        product.stock += order_products.quantity
        product.save()

        return redirect(userprofile)


#------------------------------------------------mens levis brand-------------------------------#
def levis(request):
    Cat = Categoryies.objects.get(id=1)
    brand=Brands.objects.get(brandname='Levis')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)


#------------------------------------------------mens Allen solly brand-------------------------------#
def allensolly(request):
    Cat = Categoryies.objects.get(id=1)
    brand=Brands.objects.get(brandname ='Allen Solly')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)
    

#------------------------------------------------mens peter england brand-------------------------------#
def peter(request):
    Cat = Categoryies.objects.get(id=1)
    brand=Brands.objects.get(brandname = 'Peter England' )
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)


#------------------------------------------------womens misschase brand-------------------------------#
def Miss_Chase(request):
    Cat = Categoryies.objects.get(id=2)
    brand=Brands.objects.get(brandname='Miss Chase')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)
        

#------------------------------------------------womens misschase brand-------------------------------#
def harpa(request):
    Cat = Categoryies.objects.get(id=2)
    brand=Brands.objects.get(brandname='Harpa')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)

#------------------------------------------------kids disney brand-------------------------------#
def disney(request):
    Cat = Categoryies.objects.get(id=3)
    brand=Brands.objects.get(brandname='Disney')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)    
        

#------------------------------------------------kids Puma brand-------------------------------#
def puma(request):
    Cat = Categoryies.objects.get(id=3)
    brand=Brands.objects.get(brandname='Puma')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)    
        
#------------------------------------------------kids Hopscotch brand-------------------------------#
def hopscotch(request):
    Cat = Categoryies.objects.get(id=3)
    brand=Brands.objects.get(brandname='Hopscotch')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)    
               
#------------------------------------------------kids max brand-------------------------------#
def max(request):
    Cat = Categoryies.objects.get(id=3)
    brand=Brands.objects.get(brandname='max')
    try:
        Catoffer=Categoryoffer.objects.get(category=Cat)
        co=Catoffer.discount
        if Catoffer:
            print('Cat',Catoffer,co)
    except:
        print('dddddddddddddd') 
    menproduct = Product.objects.filter(category=Cat,brand=brand)
    brand=Brands.objects.all()

    context ={
             'menproduct' : menproduct,
             'brand' : brand

        }    
    return render(request, 'menpage.html', context)    
        