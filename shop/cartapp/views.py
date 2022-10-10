from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, render
from product.models import Product
from cartapp.models import Cart, CartItem, coupon, couponuseduser
# from order.models import OrderProduct, Orders, Payment
from userside.views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    session_id = request.session.session_key
    if not session_id:
        session_id    =   request.session.create()
    return session_id

# ////////////////////////increament quantity//////////////////////////////////////////
def add_cart(request , product_id):
    
    product = Product.objects.get(id=product_id) #get the product
    rawtotal=0
    

    if request.user.is_authenticated:
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            # cart_item.cartprice += cart_item.product.offer_price()
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user)
            cart_item.save()
    else:
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart)
            cart_item.save()

    return redirect (cartview)
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////



@csrf_exempt
def add_cart_plus(request):
    id=request.POST['id']
    qty=int(request.POST['qty'])
    product = Product.objects.get(id=id) #get the product
    rawtotal=0
    print('[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')

    if request.user.is_authenticated:
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity = qty
            # cart_item.cartprice += cart_item.product.offer_price()
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = qty,user = request.user)
            cart_item.save()
    else:
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity = qty
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = qty, cart = cart)
            cart_item.save()

    return redirect (cartview)


# //////////////////////////////////////////////////////////////////////////////


def add_cartplus(request , id):
    total = 0
    quantity = 0    
    product = Product.objects.get(id=id) #get the product
    

    if request.user.is_authenticated:
        if 'coupon_code' in request.session:
            
            coupons = coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupons.discount_price

        else :
            reduction = 0
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.discount_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user,cartprice=product.discount_price() )
            cart_item.save()

        try:
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")
            
            for cart_item in cart_items:
            
                total += (cart_item.product.discount_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax -reduction
                  
        except ObjectDoesNotExist:
            pass #just ignore

        for a in cart_items:
            if a.quantity > 10 :
                a.quantity -= 10
                a.save()
            else:
                pass
        return redirect('cartview')
        print(quantity)
        print('aaaaaaaaaaaaasssssssssssssa')
        context = {
        'total':total,
        'tax':round(tax,2),
        'cart_items':cart_items,
        'quantity':quantity,
        'grand_total':grand_total
        }
    else:
        
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.discount_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart,cartprice=product.discount_price())
            cart_item.save()

        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True).order_by("-id")
            for cart_item in cart_items:
                total += (cart_item.product.discount_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax 
            
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'tax':round(tax,2),
        'cart_items':cart_items,
        'quantity':quantity,
        'grand_total':grand_total
        
        }

    return render (request,'cart.html',context)



def add_cartsimple(request , id):
    
    product = Product.objects.get(id=id) #get the product
    

    if request.user.is_authenticated:
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user,cartprice=product.offer_price())
            cart_item.save()
    else:
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.cartprice += cart_item.product.offer_price() 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart,cartprice=product.offer_price())
            cart_item.save()
    return redirect ("userhome")

@login_required(login_url='register')
def cartview(request,total = 0, quantity = 0, cart_items =None,tax = 0,grand_total =0,reduction = 0):
    rawtotal=0
    if request.user.is_authenticated:
        rawtotal=0
        if "coupon_code" in request.session:
            coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
            reduction =coupons.discount_percentage
            print(reduction,'260---')
        else:
            reduction = 0
            print('---263')
        try:
            print('265---try')
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            print(cart_items, '267')
            for cart_item in cart_items:
                print(cart_item.product.product_name , '988name88')
                print(cart_item.product.discount_price , '988discount_price88')
                print(cart_item.product.price , '988price88')
                
                if cart_item.product.discount_price != 0 | cart_item.product.discount_price != None:
                        total+= int((cart_item.product.discount_price*cart_item.quantity))
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
            tax = (2*total)/100
            grand_total = total + tax-reduction*total/100
            grand_total=round(grand_total,2)
            coupon_discount=reduction*total/100
        except ObjectDoesNotExist:
            pass #just ignore
 
    context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
            'coupon_discount': coupon_discount
            }

    return render (request,'cart.html' ,context)


# //////////////////////////decrement quantity//////////////////////////////
def remove_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.filter(product = product)
        for a in cart_items:
            if a.quantity > 1 :
                a.quantity -= 1
                a.save()
            else:
                pass
        return redirect('cartview')

    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(product = product, cart = cart)
        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.save()

        else:
            cart_items.delete()
            return redirect('cartview')
    return render (request,'cart.html')    
  
#   ///////////////////////////////////////////////////////




def remove_cartminus(request, product_id):
    print("#############################remove##########################################")
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    if request.user.is_authenticated:
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(user =request.user, product= product)

        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.save()

        else:
            cart_items.delete() 
        
    else:

        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product,id = product_id)
        cart_items = CartItem.objects.get(product= product, cart = cart)

        if cart_items.quantity > 1 :
            cart_items.quantity -= 1
            cart_items.cartprice -= cart_items.product.discount_price() 
            cart_items.save()

        else:
            cart_items.delete()

    if request.user.is_authenticated:

        if 'coupon_code' in request.session:
            
            coupons = coupon.objects.get(coupon_code =request.session['coupon_code'])
            reduction = coupons.discount_price

        else :
            reduction = 0

        
        try:
            
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")
            
            for cart_item in cart_items:
            
                total += (cart_item.product.offer_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax -reduction
            if grand_total <0:
                grand_total = tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':round(tax,2),
        'grand_total':grand_total,
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True).order_by("-id")
            for cart_item in cart_items:
                total += (cart_item.product.discount_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':round(tax,2),
        'grand_total':grand_total,
        }

    return render (request,'cart.html',context)



#   //////////////////////////////////////////////////////


def delete_carts(request, id):
    total = 0
    quantity = 0
    rawtotal=0
    discount_price=0

    cart_items = CartItem.objects.get(id =id )
    cart_items.delete()

    if request.user.is_authenticated:
        try:
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True).order_by("-id")
            
            for cart_item in cart_items:
                if cart_item.product.discount_price>0:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
            tax = (2*total)/100
            grand_total = total + tax - discount_price
                  
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'cart_items':cart_items,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total,
        
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True)
            for cart_item in cart_items:
                if cart_item.product.discount_price>0:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
            tax = (2*total)/100
            grand_total = total + tax
            
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'tax':tax,
        'cart_items':cart_items,
        'quantity':quantity,
        
        }
    return render (request,'cart.html',context)

        


def delete_cart_product(request,product_id, cart_id):
    
        product=Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get( id = cart_id,product=product)
        print(cart_item)
        cart_item.delete()

        return Jsonresponse({'success' : True}, safe= False)
# ////////////////////////////////cartitem delete/////////////////////////////////////////
def delete_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get( product=product,user=request.user)
    cart_item.delete()
    return redirect(cartview)

# //////////////////////////////////////////////apply coupon /////////////////////////////////////
def apply_coupon(request):
    print("SDFGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    if request.method == "POST":
        coupon_code =request.POST.get("coupon_code")
        print(coupon_code)
        try:
            if coupon.objects.get(coupon_code=coupon_code):
                coupon_exist= coupon.objects.get(coupon_code=coupon_code)

                print(coupon_exist)
                try:            
                    if couponuseduser.objects.get(user=request.user,coupon=coupon_exist):
                        messages.error(request, "coupon already applied")
                        return redirect(checkout)
                except:
                    request.session["coupon_code"]=coupon_code
            else:
                messages.error(request, "coupon already don't exists")
                return redirect(checkout)
                
        except:
            messages.error(request, "coupon  don't exists")

    return redirect(checkout)