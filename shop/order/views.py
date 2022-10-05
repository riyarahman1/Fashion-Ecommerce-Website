from datetime import date
import re
from django.shortcuts import render
from datetime import date
import datetime
import razorpay
from django.conf import settings
from cartapp.models import CartItem,coupon,couponuseduser
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render,get_object_or_404,reverse
from accounts.models import Address
from order.models import Order, Payment,OrderProduct
from product.models import Product
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.


def confirmpayment(request,total = 0, quantity = 0, cart_items =None,tax = 0,grand_total =0,coupon_discount=0):
    rawtotal=0
    
    if request.method == "POST":
        global theaddress
        theaddress = request.POST.get('address_id') #address object in the address as we passed address in it
    if theaddress == None:
        return redirect("checkout")

    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    details =None
    # theaddress =None
    theaddress = request.POST.get('address_id') #address object in the address as we passed address in it
    print(theaddress)
    if request.user.is_authenticated:
         
         
        if "coupon_code" in request.session:
            coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
            reduction =coupons.discount_percentage
            # print('couponnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
            
        else:
            reduction = 0
     
        try:
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            print(cart_items)
            print(theaddress)
            print("eeeeeeeeeeeeeee")
            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            print(details)
            for cart_item in cart_items:
                if cart_item.product.discount_price is not None:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
            tax = (2*total)/100
            grand_total = total + tax-reduction*total/100
            coupon_discount=reduction*total/100

            if grand_total <0:
                grand_total = tax
            print('couponnnnnnnnnn')
            
        except ObjectDoesNotExist:
            pass #just ignore
        new_total=grand_total*100
        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'details':details,
        "new_total":new_total,
        'coupon_discount': coupon_discount
        }
        print(cart_items)
        print(cart_items)

        print(tax)
        print(total)
    else:
        return redirect("cartview")
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    # client = razorpay.Client(auth=("rzp_test_Hc2RcWF8IFsvhC", "755UrbHZBILicM1XPyh9SVcJc"))
    print(grand_total)
    print(new_total)


    print("sdvhcjbcbbbbbbbbbbbbb")
    global payments
    payments =client.order.create({"amount":int(grand_total)*100, "currency" : "INR", "payment_capture":1})
    # print(payments.amount)

    payment_id = payments["id"]
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if "coupon_code" in request.session:
            try:
                coupon_useduser=couponuseduser(coupon=coupons,user=request.user)
                coupon_useduser.save()
            except:
                pass
    if "coupon_code" in request.session:
        del request.session["coupon_code"] 

    return render(request,'orderpage.html',context)


# //////////////////////////////////////////////////////////////////COD/////////////////////////////////////////////////////////////////////////////////////////////////////////////

def placecod(request):

    rawtotal=0
    
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    order_id_generated=0
    if request.user.is_authenticated:

        if "coupon_code" in request.session:
            coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
            reduction =coupons.discount_percentage
        else:
            reduction = 0
        try:

            details = Address.objects.get(id = theaddress ) #passed that specific address in the details variable
            print('couponnnnnnnnnnnnnnnnn')
            
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            print(order_id_generated)
            print("RRRRRRRrrrrrrrrrrrrrrrrrrrrr")
            user =  request.user
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            cart_itemcount = cart_items.count()
            if cart_itemcount <= 0 :
                return redirect("index")
            for cart_item in cart_items:
                if cart_item.product.discount_price is not None:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
            tax = (2*total)/100
            grand_total = total + tax-reduction*total/100
            if grand_total <0:
                grand_total = tax
                

            dates =date.today()   
            paymethod = 'COD'
            pay = Payment(user=request.user,payment_method =paymethod,amount_paid=grand_total ,status='Pending',created_at=dates)
            pay.save()
            
            oder = Order(user=user,address=details ,ordertotal = total,orderid =order_id_generated,date=dates,payment =pay)
            print('couponnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')

            oder.save()

            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            
            


       

            for x in cart_items:
                Orderproduct = OrderProduct(order=oder,user=request.user)
                product = Product.objects.get(id = x.product.id)
                Orderproduct.product = x.product
                
                Orderproduct.quantity = x.quantity
                Orderproduct.price = x.product.price * x.quantity
                print(x.cartprice)
                print(Orderproduct.price)
                print("********************************")

                print(product.stock)
                print("********************************")

                print(x.quantity)
                print("********************************")
                product.stock -=  x.quantity
                product.save()
                Orderproduct.save()
                print( Orderproduct.price )
                print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")

            for x in cart_items:
                x.delete()
            
            

        except ObjectDoesNotExist:
           
            pass #just ignore

        
        

    else:
        return redirect('cartview')
    if "coupon_code" in request.session:
        try:
            coupon_useduser=couponuseduser(coupon=coupons,user=request.user)
            coupon_useduser.save()
        except:
            pass
    # order = Order.objects.get(orderid = order_id_generated)
    # order.is_ordered = True
    # order.save()
    Orderproduct = OrderProduct.objects.filter(order=oder)
    print(Orderproduct)
    context = {
    'total':total,
    'quantity':quantity,
    'orderproduct':Orderproduct,
    'tax':tax,
    'grand_total':pay.amount_paid,
    'details':details,
        }

    if "coupon_code" in request.session:
            del request.session["coupon_code"] 
    # return HttpResponse ("Payment success thanks for the order")
    return render(request,'bill.html',context)
     


    #  ///////////////////////////////////////////////////////////////////////razorpay //////////////////////////////////////////////////////////////////////////////////////
    
def razorpay_sucess(request):
   rawtotal=0
   carts_items=None
   if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
   else:
        reduction = 0

   # order_id = request.GET.get("order_id")
   carts_items  = CartItem.objects.filter(user = request.user, is_active = True)
   cart_itemcount = carts_items.count()
   if cart_itemcount <= 0 :
        return redirect ("index")
   total=0
   quantity=0
   user=request.user
   for cart_item in carts_items:
                if cart_item.product.discount_price is not None:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
                tax = (2*total)/100
                grand_total = total + tax-reduction
   if reduction > 0:
        new_total= total-reduction*total/100

   else:
        new_total=total



   order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   dates =date.today()
   amount = new_total
   payment_method="razorpay"
   payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   payments = Payment(user=user,payment_id=payment_id,payment_method=payment_method,amount_paid=amount,created_at=dates)
   payments.save()
   details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable

   orders = Order(user=user,orderid=order_id_generated,address=details,ordertotal=new_total,date=dates,payment=payments)
   orders.save()
   ordered_products = OrderProduct.objects.filter(order = orders)

   cart_items  = CartItem.objects.filter(user = request.user)
   for x in cart_items:
        print(orders)       
        Orderproduct = OrderProduct(order=orders)
        Orderproduct.user=user
        Orderproduct.payment=payments
        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.product_price = x.product.price * x.quantity
        Orderproduct.save()
   if "coupon_code" in request.session:
        try:
            coupon_useduser=couponuseduser(coupon=coupon,user=request.user)
            coupon_useduser.save() 
        except:
            pass
   carts_items.delete()
   print(Orderproduct)
   print("fffffffffffffffffffffffffffff")
   Orderproduct = OrderProduct.objects.filter(order=orders)

   if "coupon_code" in request.session:
        del request.session["coupon_code"] 
   context = {
                'total':amount,
    'quantity':quantity,
    'orderproduct':Orderproduct,
    'tax':tax,
    'grand_total':grand_total,
    'details':details,
   }
#    return HttpResponse ("Payment success thanks for the order")

   return render (request,"bill.html",context)

# //////////////////////////////////////////paypal//////////////////////////////////

def paypal(request):
    rawtotal=0

    # order = get_object_or_404(Order)
    host = request.get_host()

    if "coupon_code" in request.session:
            coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
            reduction =coupons.discount_percentage
    else:
            reduction = 0

    # order_id = request.GET.get("order_id")
    carts_items  = CartItem.objects.filter(user = request.user, is_active = True)
    cart_itemcount = carts_items.count()
    if cart_itemcount <= 0 :
            return redirect ("index")
    total=0
    quantity=0
    user=request.user
    for cart_item in carts_items:
                if cart_item.product.discount_price is not None:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
                tax = (2*total)/100
                grand_total = total + tax-reduction*total/100
    if reduction > 0:
            new_total= total-reduction*total/100

    else:
            new_total=total
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': grand_total,
        # 'item_name': 'Order {}'.format(order.id),
        # 'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'paypal.html', {'form': form})




@csrf_exempt
def payment_done(request):
   rawtotal=0

   if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
   else:
        reduction = 0

   # order_id = request.GET.get("order_id")
   carts_items  = CartItem.objects.filter(user = request.user, is_active = True)
   cart_itemcount = carts_items.count()
   if cart_itemcount <= 0 :
        return redirect ("index")
   total=0
   quantity=0
   user=request.user
   for cart_item in carts_items:
                if cart_item.product.discount_price>0:
                        total+=(cart_item.product.discount_price*cart_item.quantity)
                        quantity+=cart_item.quantity
                else:
                        total+=(cart_item.product.price*cart_item.quantity)
                        quantity+=cart_item.quantity
                rawtotal+=(cart_item.product.price*cart_item.quantity)
                
                tax = (2*total)/100
                grand_total = total + tax-reduction*total/100
   if reduction > 0:
        new_total= total-reduction*total/100

   else:
        new_total=total



   order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   dates =date.today()
   amount = new_total
   payment_method="paypal"
   payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   payments = Payment(user=user,payment_id=payment_id,payment_method=payment_method,amount_paid=amount,created_at=dates)
   payments.save()
   details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable

   orders = Order(user=user,orderid=order_id_generated,address=details,ordertotal=new_total,date=dates,payment=payments)
   orders.save()
   ordered_products = OrderProduct.objects.filter(order = orders)

   cart_items  = CartItem.objects.filter(user = request.user)
   for x in cart_items:
        print(orders)       
        Orderproduct = OrderProduct(order=orders)
        Orderproduct.user=user
        Orderproduct.payment=payments
        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.product_price = x.product.price * x.quantity
        Orderproduct.save()
   if "coupon_code" in request.session:
        try:
            coupon_useduser=couponuseduser(coupon=coupon,user=request.user)
            coupon_useduser.save() 
        except:
            pass
   carts_items.delete()
   print(Orderproduct)
   Orderproduct = OrderProduct.objects.filter(order=orders)

   if "coupon_code" in request.session:
        del request.session["coupon_code"] 
   context = {
                'total':amount,
    'quantity':quantity,
    'orderproduct':Orderproduct,
    'tax':tax,
    'grand_total':grand_total,
    'details':details,
   }

   return render(request, 'bill.html',context)


@csrf_exempt
def payment_canceled(request):
   

    return render(request, 'failed.html')

#    //////////////////////////////////////////////////////////////////////paypal///////////////////////////////////////////////////////////////////////////////////

# def paypal(request):
#     # preview_page view
 
#     reduction = 0
        
#     if request.user.is_authenticated:
#         try:
        
#             carts_item = cart_item.objects.filter(
#                 user=request.user, is_active=True
#             ).order_by("id")
#             if not carts_item:
#                 return redirect ("index_page")

#             cart_itemcount = carts_item.count()
#             if cart_itemcount <= 0 :
#                 return redirect ("index_page")
                
#             total=0
#             quantity=0
      
#             for item in carts_item:
#                 total += offer_check(item) * item.quantity
#                 quantity += item.quantity
#             if reduction > 0:
#                 new_total= total-reduction*total/100
#             else:
#                 new_total=total
            
#             order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
#             dates =date.today()
#             orders = order(user=request.user,address=addresss ,total = new_total,order_id =order_id_generated,date=dates)
#             order_products = order_product.objects.filter(order=orders)
#             orders.save()
#         except ObjectDoesNotExist:
#                pass #just ignore
#     else:
#         return redirect(cart_view)
   
   
#     values ={"carts_item":carts_item,"total":new_total,"quantity":quantity,"orders":orders,"order_products":order_products,}
   
#     return render (request,"paypal.html",values)
#     # ///////////////////////////////////////////////////////////////////////////////////////////////////////
#     def payments(request):
#     user=request.user
#     # if request.session.get('posted_page_visited'):
#     #     del request.session['posted_page_visited']
#     #     # return http.HttpResponseRedirect("form_page")
#     #     return HttpResponse ("Payment success thanks for the orderaaa")
#     body = json.loads(request.body)
#     print(body['orderID'])

#     orders = order.objects.get( order_id = body['orderID'] )
#     payments = payment(

#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount = orders.total,
#         # status = body['status'],
#     )
#     payments.save()
#     print(body)
#     print(orders.order_id)
#     # print(orders.payments.payment_id)

#     orders.payment = payments
#     orders.is_ordered =True
#     orders.save()
#     print(orders)       


#     #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
#     cart_items  = cart_item.objects.filter(user = request.user)
#     print(cart_items)
#     for x in cart_items:
#         print(orders)       
#         Orderproduct = order_product(order=orders)
#         print(Orderproduct)
#         Orderproduct.user=user
#         Orderproduct.product = x.product
#         Orderproduct.quantity = x.quantity
#         Orderproduct.product_price = offer_check(x)
#         Orderproduct.save()
#     #REDUCE THE QUANTITY OF STOCK

#         product = products.objects.get(id = x.product.id)
#         product.stock -= x.quantity
#         product.save()
#     #CLEAR CART
#     for x in cart_items:
#         x.delete()

#     #SEND ORDER RECIEVED EMAIL TO CUSTOMER
    



#     #SEND ORDER NUMBER AND TRANSACTION ID BACK TO SEND DATA METHOD VIA JASON RESPONDS
#     data = {
#         "orderID":orders.order_id,
#         "transID":payments.payment_id,
#     }

#     return JsonResponse(data)


# @cache_control(no_cache =True, must_revalidate =True, no_store =True)   
# def order_complete(request):
#     user =request.user
#     total = 0
#     quantity = 0
#     cart_items =None
#     tax = 0
#     grand_total =0
#     order_number    = request.GET.get("orderID")
#     transID         = request.GET.get("transID")
# #     print(order_number)
# #     if "coupon_code" in request.session:
# #         coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
# #         reduction =coupons.discount_percentage
# #     else:
# #         reduction = 0
# #     try:
# #         dates =date.today()  

# #         addresss = address.objects.get(id = address_id )
# #         payment_method = "paypal"
        
# #         payments = payment(user=request.user,payment_id=order_number,payment_method=payment_method,amount=grand_total,date=dates)
# #         payments.save()
# #         orders = order.objects.get(order_id = order_number)
# #         orders.payment=payments
# #         orders.save()

# #         ordered_products = order_product.objects.filter(order = orders)
# #         print(ordered_products)
        

#         # print(ordered_products)
#         # for cart_item in ordered_products:
#         #     total += (offer_check(cart_item) * cart_item.quantity)
#         #     quantity += cart_item.quantity
#         #     cart_item.payment=payments
#         #     cart_item.save()
#         # tax = (2*total)/100
#         tax = 0
#         grand_total = total + tax
#         if reduction > 0:
#             new_total= total-reduction*total/100
#         else:
#             new_total=total
       
       
#         print(orders)
#         context = {
#             "payments":payments,
#             "order":orders,
#             "ordered_products":ordered_products,
#             "orderID":orders.order_id,
#             "addresss":addresss,
#             "transID":transID,
#             "dates":dates,
#             "total":total,
#             "tax":tax,
#             "total":new_total,
#             "quantity":quantity,
#             "reduction":reduction,
#             "new_total":new_total
            
#         }
#         # # request.session['posted_page_visited'] = True
#         # if "coupon_code" in request.session:
#         #     try:
        #         coupon_useduser=couponuseduser(coupon=coupons,user=request.user)
        #         coupon_useduser.save()
        #     except:
        #         pass
        # if "coupon_code" in request.session:
        #     del request.session["coupon_code"] 


    #   return render(request,"index.html" )
    #     return render (request,"order_conforme.html",context)

    # except (payment.DoesNotExist,order.DoesNotExist):
    #              return redirect ("index_page")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
