from .models import Cart, CartItem, coupon
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def extras(request,total = 0, quantity = 0, cart_items =None,tax = 0,grand_total =0):    
    if request.user.is_authenticated:
        
        try:
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'totals':total,
        'quantitys':quantity,
        'cart_itemss':cart_items,
        'taxs':tax,
        'grand_totals':grand_total,
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'totals':total,
        'quantitys':quantity,
        'cart_itemss':cart_items,
        'taxs':tax,
        'grand_totals':grand_total,
        }
    
    return dict(context)

