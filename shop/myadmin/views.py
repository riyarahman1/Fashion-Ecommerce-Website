from multiprocessing import context

from requests import request
from accounts.models import Account
from category.models import Categoryies , Brands
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from product.models import Product
from order.models import Order,OrderProduct,Payment
from django.core.paginator import Paginator
from django.db.models import Sum,Count
from cartapp.models import CartItem,coupon,couponuseduser
from product.models import *
from datetime import date
import datetime

# Create your views here.
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signinadmin(request):
    print('ffas')
    if 'username' in request.session:
         return redirect(admin_home)
         print('ffas')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('ffas')
        user = authenticate(username = username,password=password)

        if user is not None and user.is_superuser:
            request.session['username'] = username
            login(request,user)
            return redirect(admin_home)
            # if user.is_superuser:
            #     request.session['username']=username
            #     login(request,user)
            #     return redirect(admin_home)
        else:
            messages.error(request,'invalid credentials')
            return redirect(signinadmin)

    return render (request,'adminside/adminlogin.html')


# @cache_control(no_cache =True, must_revalidate =True, no_store =True)
# def admin_home(request):
#     return render (request,'admindashboard.html')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_logout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(signinadmin) 


# ---------------------------- user_list ---------------------------- #

def user_list(request):
    theuser = Account.objects.all()
    paginator=Paginator(theuser,per_page=5)
    page_number=request.GET.get('page')
    userfinal=paginator.get_page(page_number)
    totalpage=userfinal.paginator.num_pages
    context={
        'theuser':userfinal,
        'lastpage':totalpage,
        'totalPagelist':[n +1 for n in range(totalpage)]
    }
   


    print(theuser)
    return render (request,'adminside/userlist.html',context)   

# ---------------------------- block_user ---------------------------- #

def block_user(request,id):
    x=Account.objects.get(id=id)
    if x.is_active:
        x.is_active=False

    else:
        x.is_active=True
    
    x.save()         
    return redirect(user_list)

# ------------------------------ product management------------------------------ #
# ---------------------------product  -------------------------- #

def product(request):
    theproduct = Product.objects.all().order_by('-id')
    paginator=Paginator(theproduct,per_page=4)
    page_number=request.GET.get('page')
    productfinal=paginator.get_page(page_number)
    totalpage=productfinal.paginator.num_pages
    context={
            'theproduct':productfinal,
            'lastpage':totalpage,
            'totalpagelist':[n+1 for n in range(totalpage)]
        }
    return render (request,'adminside/product.html',context)

# ---------------------------deleteproduct -------------------------- #

def deleteproduct(request,id):
    deleteproduct =Product.objects.get(id=id)
    deleteproduct.delete()
    return redirect(product)

# -------------------------- add product -------------------------- #

def addproduct(request):
    values = Categoryies.objects.all()
    brand = Brands.objects.all()
         
    context={
            'values':values,
            'brand':brand,
        }
    print(request.POST)
    if request.method =='POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        print(brand,'brand')
        if name=="":
                messages.error(request,"Name is Empty")
                return render(request,'adminside/addproduct.html',context)     
        elif description=="":
                messages.error(request,"Description is Empty")
                return render(request,'adminside/addproduct.html',context)  
        elif len(description)<5:
                messages.error(request,"Description is too short")
                return render(request,'adminside/addproduct.html',context)  
        elif brand=="":
                messages.error(request,"brand is Empty")
                return render(request,'adminside/addproduct.html',context)   
         
        x = Categoryies.objects.get(id=category)
        y = Brands.objects.get(id=brand)
        prod=Product(product_name=name,description=description,price=price,stock=stock,category=x,brand=y,image=image,image1=image1,image2=image2,image3=image3)
        
        prod.save()
        messages.success(request,"Product Added Successfully")
        return redirect(product)
        
   
    return render(request,'adminside/addproduct.html',context)  

# ---------------------------edit product -------------------------- #

def editproduct(request,id):
    this_product = Product.objects.get(id=id)
    values = Categoryies.objects.all()
    brand = Brands.objects.all()

    if request.method == 'POST':

        product_name = request.POST.get('name')
        product_description = request.POST.get('description')
        product_price  = request.POST.get('price')
        product_stock  = request.POST.get('stock')
        product_brand = request.POST.get('brand')
        product_image  = request.FILES.get('image')
        product_image1 = request.FILES.get('image1')
        product_image2 = request.FILES.get('image2')
        product_image3 = request.FILES.get('image3')
        if product_name=="":
                messages.error(request,"Name is Empty")
                return render(request,'adminside/editproduct.html')     
        elif product_description=="":
                messages.error(request,"Description is Empty")
                return render(request,'adminside/addproduct.html')  
        elif len(product_description)<5:
                messages.error(request,"Description is too short")
                return render(request,'adminside/addproduct.html')   
        elif product_brand=="":
                messages.error(request,"brand is Empty")
                return render(request,'adminside/addproduct.html')    
         
        obj = Product.objects.get(id=id)
        obj.product_name = product_name
        obj.description = product_description
        obj.price = product_price
        obj.stock = product_stock
        obj.image = product_image
        obj.Brand = product_brand
        obj.image1 = product_image1
        obj.image2 = product_image2
        obj.image3 = product_image3

    # if product_name == "" or product_description == "" or  product_price == "" or  product_stock == "" or product_image == "" or product_image1 == "" or product_image2 == "" or  product_image3 == "":
    #     messages.error(request, "Fill all Fields")
    # else:
        obj.save()
        return redirect(product)
    return render(request,'adminside/editproduct.html',{'this_product': this_product,'values':values,'brand':brand})      


# ------------------------------ Category management------------------------------ #
# ---------------------------  category -------------------------- #

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def categoryList(request):
    if 'username' in request.session:
        thecategory = Categoryies.objects.all()  
        paginator=Paginator(thecategory,per_page=3)
        page_number=request.GET.get('page')
        categoryfinal=paginator.get_page(page_number)
        totalpage=categoryfinal.paginator.num_pages
        context={
            'thecategory':categoryfinal,
            'lastpage':totalpage,
            'totalpagelist':[n+1 for n in range(totalpage)]
        }
        return render(request,'adminside/categories.html',context)
    return redirect(signinadmin)
    
    # ///////////////////////////////////////////////////////////////




    # ---------------------------addcategory -------------------------- #

def addcategory(request):
    values = Categoryies.objects.all()
    if request.method =='POST':
        name = request.POST.get('name')
        if name=="":
                messages.error(request,"Name is Empty")
                return render(request,'adminside/Addcategory.html')     
    
        if Categoryies.objects.filter(category_name=name):
            messages.error(request,"Category already exists")
            return render(request,'adminside/Addcategory.html',{'values':values})      

        description = request.POST.get('description')
        variables = Categoryies(category_name=name,description=description)
      
        variables.save()
        return redirect(categoryList)
    return render(request,'adminside/Addcategory.html',{'values':values})      

    # ---------------------------editcategory -------------------------- #

def editcategory(request,id):
    values = Categoryies.objects.get(id=id)
    if request.method =='POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        cat =Categoryies.objects.get(id=id)
        cat.name=name
        cat.description= description
        cat.save()

        if name=="":
                messages.error(request,"Name is Empty")
                return render(request,'adminside/editcategory.html')     
        return redirect(categoryList)
        
    return render(request,'adminside/editcategory.html',{'values':values})      

# -------------------------- deletecategory -------------------------- #

def deletecategory(request,id):
    my_cat = Categoryies.objects.get(id=id)
    my_cat.delete()
    return redirect(categoryList) 



# ----------------------------brand-------------------------#

def brandlist(request):
    if 'username' in request.session:
        thebrand = Brands.objects.all()  
        paginator=Paginator(thebrand,per_page=3)
        page_number=request.GET.get('page')
        brandfinal=paginator.get_page(page_number)
        totalpage=brandfinal.paginator.num_pages
        context={
            'thebrand':brandfinal,
            'lastpage':totalpage,
            'totalpagelist':[n+1 for n in range(totalpage)]
        }
        return render(request,'adminside/brand.html',context)
    return redirect(signinadmin)


#---------------------------------add brand------------------------------------#

def addbrand(request):
    values =Brands.objects.all()
    if request.method =='POST':
        brandname = request.POST.get('brandname')
        if brandname=="":
                messages.error(request,"Brand is Empty")
                return render(request,'adminside/Addbrand.html')     
    
        if Brands.objects.filter(brandname=brandname):
            messages.error(request,"Brand already exists")
            return render(request,'adminside/Addbrand.html',{'values':values})      

       
        variables = Brands(brandname=brandname)
      
        variables.save()
        return redirect(brandlist)
    return render(request,'adminside/Addbrand.html',{'values':values})   

# #----------------------------------edit brand--------------------------------#
    
def editbrand(request,id):
    values = Brands.objects.get(id=id)
    if request.method =='POST':
        brandname = request.POST.get('brandname')
        brand =Brands.objects.get(id=id)
        brand.name=brandname
        brand.save()

        if brandname=="":
                messages.error(request,"Brand is Empty")
                return render(request,'editbrand.html')     
        return redirect(brandlist)
        
    return render(request,'adminside/editbrand.html',{'values':values})      
  

#-----------------------------------delete brand------------------------#
def deletebrand(request,id):
    my_brand = Brands.objects.get(id=id)
    my_brand.delete()
    return redirect(brandlist) 


# ------------------------------ productlist managemnet ------------------------------ #
# --------------------------- mensproduct -------------------------- #

def adminmen(request):
     adminmens = Product.objects.filter(category="1")
     paginator=Paginator(adminmens,per_page=3)
     page_number=request.GET.get('page')
     menfinal=paginator.get_page(page_number)
     totalpage=menfinal.paginator.num_pages
     context={
        'adminmens':menfinal,
        'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
     }
     return render (request,'adminside/adminmen.html',context)

# --------------------------- womensproduct -------------------------- #

def adminwomen(request):
    adminwomens = Product.objects.filter(category="2")
    paginator=Paginator(adminwomens,per_page=3)
    page_number=request.GET.get('page')
    womenfinal=paginator.get_page(page_number)
    totalpage=womenfinal.paginator.num_pages
    context={
        'adminwomens':womenfinal,
        'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
     }
    return render (request,'adminside/adminwomen.html',context)     

# --------------------------- kidsproduct -------------------------- #

def adminkids(request):
     adminkid = Product.objects.filter(category="3")
     paginator=Paginator(adminkid,per_page=4)
     page_number=request.GET.get('page')
     kidfinal=paginator.get_page(page_number)
     totalpage=kidfinal.paginator.num_pages
     context={
        'adminkid':kidfinal,
        'lastpage':totalpage,
        'totapagelist':[n+1 for n in range(totalpage)]
     }
     return render (request,'adminside/adminkids.html',context) 
            
# ------------------------------order management ------------------------------ #
# --------------------------- order -------------------------- #


def order_management(request):
    orderproduct =None
    orders=None
   
    orderproduct=OrderProduct.objects.all().order_by("-id")
    orders = Order.objects.all().order_by("-date")
    paginator=Paginator(orders,per_page=4)
    page_number=request.GET.get('page')
    orderfinal=paginator.get_page(page_number)
    totalpage=orderfinal.paginator.num_pages
    context={
        'orders':orderfinal,
        'orderproduct':orderproduct,
        'lastpage':totalpage,
        'totapagelist':[n+1 for n in range(totalpage)]
     }
    return render(request,"adminside/order.html",context)  

# --------------------------change payment status -------------------------- #

def change_status(request,id):
    if "username" in request.session:
        if request.method == "POST":
            status = request.POST.get("status")
            orders = Order.objects.get(id=id)
            orders.status= status
            print(status)
            orders.save()
            return redirect(order_management)

# --------------------------- productorders -------------------------- #

def product_order_management(request,id):
    if "username" in request.session:
        orders = Order.objects.get(id=id)
        orderproduct=OrderProduct.objects.filter(order=orders)
        return render(request,"adminside/product_order_management.html",{"orderproduct":orderproduct,"orders":orders})  
        
# --------------------------- product status -------------------------- #

def product_change_status(request,id):
    if "username" in request.session:
        if request.method == "POST":
            status = request.POST.get("status")
            orderproduct = OrderProduct.objects.get(id=id)
            orderproduct.status= status
            print(status)
            orderproduct.save()
            return redirect(order_management)   
# --------------------------- admin home -------------------------- #
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_home(request):
        order = Payment.objects.filter(payment_method = 'COD')
        codtotal = 0
        cod = 0
        for ord in order:
            codtotal = codtotal+float(ord.amount_paid)
            cod+= 1

        raz = 0
        order = Payment.objects.filter(payment_method = 'razorpay')   
        raztotal = 0
        for ord in order:
            raztotal = raztotal+float(ord.amount_paid) 
            raz+= 1
            
        order = Payment.objects.filter(payment_method = 'paypal')   
        paytotal = 0
        pay = 0
        for ord in order:
            paytotal = paytotal+float(ord.amount_paid) 
            pay+= 1

        total =  paytotal + raztotal +  codtotal

        context = {
            # 'orders':orders,
            'codtotal':codtotal,
            'paytotal':paytotal,
            'raztotal':raztotal,
            'total':total,
            # 'pay':pay,
            'raz':raz,
            'cod':cod
        }
       
        # context = {
        #     'orders':orders,
        #     'codtotal':codtotal,
        #     'paytotal':paytotal,
        #     'raztotal':raztotal,
        #     'total':total,
        #     'pay':pay,
        #     'raz':raz,
        #     'cod':cod
        # }
    # print(paytotal)
        if 'username' in request.session:
            return render(request, "adminside/admindashboard.html",context)
        else:
            return redirect(signinadmin)


# ------------------------------ Coupon Offer ------------------------------ #
# --------------------------- viewcoupon offer -------------------------- #
def view_coupon(request):
    coupons =coupon.objects.all().order_by("id")
    return render(request, "adminside/view_coupon.html",{"coupons":coupons})

# --------------------------- usedcoupon -------------------------- #

def view_couponuseduser(request):
    coupon_useduser=couponuseduser.objects.all().order_by("id")
    return render(request, "adminside/view_couponuseduser.html",{"coupon_useduser:coupon_useduser"})

# --------------------------- addcoupon-------------------------- #

def add_coupon(request):
    if request.method == "POST":
        coupon_code =request.POST.get("coupon_code")
        discount_percentage =request.POST.get("discount_price")
        
        try:
            discount= int(discount_percentage)
            if discount > 0 :
                if discount <100:
                    coupons=coupon(coupon_code=coupon_code,discount_percentage=discount)
                    coupons.save()
                    return redirect(view_coupon)
        except:
            messages.success(request,"cant repeat same coupon and offer must be between 1 to 90%")
            return render(request, "add_coupon.html")
                     
    return render(request, "adminside/add_coupon.html")
         
# ---------------------------addcoupon -------------------------- #

def block_coupon(request, id):
    coupons = coupon.objects.get(id=id)
    if coupons.is_active:
        coupons.is_active = False
    else:
        coupons.is_active = True
    coupons.save()
    return redirect(view_coupon)

# --------------------------- delete coupon-------------------------- #

def delete_coupon(request,id):
    coupons = coupon.objects.get(id=id)
    coupons.delete()
    return redirect(view_coupon)


# ------------------------------ Category Offer ------------------------------ #
# --------------------------- Adding category offer -------------------------- #

def New_CategoryOffer(request):
    CategoryObj=Categoryies.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        category=request.POST.get("category_name")
        print("discount",discount)
        if discount =='':
            messages.error(request,"discount field should not be empty")
            return redirect(New_CategoryOffer)
        discount=int(discount)
        if Categoryoffer.objects.filter(category=category).exists():
            messages.error(request,"Offer already exists for this Category")
            return redirect(View_CategoryOffers)
        if discount>0:
            if discount<90:
                
                newCategoryOffer=Categoryoffer()
                newCategoryOffer.discount=discount
                newCategoryOffer.category=Categoryies.objects.get(id=category)
                newCategoryOffer.save()
                return redirect(View_CategoryOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_CategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_CategoryOffer)
    return render(request,'adminside/Add_NewCategoryOffer.html',{'Category':CategoryObj})

# ---------------------------- Edit CategoryOffer ---------------------------- #

def Edit_CategoryOffer(request,id):
    CategoryObj=Categoryies.objects.all()
    CategoryOfferObj=Categoryoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        category=request.POST.get("category_name")
        discount=int(discount)
        print(category)
        print("Kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        if discount>0:
            if discount<90:
                CategoryOfferObj.discount=discount
                CategoryOfferObj.category=Categoryies.objects.get(category_name=category)
                CategoryOfferObj.save()
                return redirect(View_CategoryOffers)
      
            else:
                context={
                         'Category':CategoryObj,
                            'CategoryOffer':CategoryOfferObj
                         }
                messages.error(request,"Discount must be less than 90%")
                return render(request,'adminside/Edit_CategoryOffer.html',context)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(Edit_CategoryOffer)
    context={
        'Category':CategoryObj,
        'CategoryOffer':CategoryOfferObj
    }
    return render(request,'adminside/Edit_CategoryOffer.html',context)



# --------------------------- View category Offers --------------------------- #
def View_CategoryOffers(request):
    CategoryOfferObj=Categoryoffer.objects.all()
    paginator=Paginator(CategoryOfferObj,per_page=2)
    page_number=request.GET.get('page')
    CategoryOfferObjfinal=paginator.get_page(page_number)
    totalpage=CategoryOfferObjfinal.paginator.num_pages
    context={
        'CategoryOffer':CategoryOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'adminside/View_CategoryOffer.html',context)

# -------------------------- Delete A Category Offer ------------------------- #
def Delete_CategoryOffer(request,id):
    toDelete_CategoryOffer=Categoryoffer.objects.get(id=id)
    toDelete_CategoryOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_CategoryOffers)

# ---------------------------- Block CategoryOffer --------------------------- #
def Block_CategoryOffer(request,id):
    toBlock_CategoryOffer=Categoryoffer.objects.get(id=id)
    toBlock_CategoryOffer.is_active=False
    toBlock_CategoryOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_CategoryOffers)

# --------------------------- Unblock CategoryOffer -------------------------- #
def UnBlock_CategoryOffer(request,id):
    toUnBlock_CategoryOffer=Categoryoffer.objects.get(id=id)
    toUnBlock_CategoryOffer.is_active=True
    toUnBlock_CategoryOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_CategoryOffers)    

# ------------------------------ Product Offer ------------------------------ #
# --------------------------- Adding Product  offer -------------------------- #

def New_ProductOffer(request):
    products=Product.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        choosed_product=request.POST.get("product_name")
        if discount =='':
            messages.error(request,"discount field should not be empty")
            return redirect(New_ProductOffer)
        discount=int(discount)
        if Productoffer.objects.filter(product=choosed_product).exists():
            messages.info(request,"Offer already exists for this Product")
            return redirect(View_ProductOffers)
        discount=int(discount)
        if discount>0:
            if discount<90:
                newProductOffer=Productoffer()
                newProductOffer.discount=discount
                # newProductOffer.product=Product.objects.get(id=choosed_product)
                product=Product.objects.get(id=choosed_product)
                product.discount_price=(product.price-(product.price*discount/100))
                print('product',product.discount_price)
                product.save()
                print('product',product.discount_price)
                newProductOffer.product=Product.objects.get(id=choosed_product)
                newProductOffer.save()
                return redirect(View_ProductOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_ProductOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_ProductOffer)
    return render(request,'adminside/Add_NewProductOffer.html',{'Products':products})

# # ---------------------------- Edit ProductOffer ---------------------------- #

def Edit_ProductOffer(request,id):
    products=Product.objects.all()
    ProductOfferObj=Productoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        choosed_product=request.POST.get("product_name")
        discount=int(discount)
        if discount>0:
            if discount<90:
                ProductOfferObj.discount=discount
                ProductOfferObj.category=Product.objects.get(product_name=choosed_product)
                ProductOfferObj.save()
                return redirect(View_ProductOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(Edit_ProductOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(Edit_ProductOffer)
    context={
        'Products':products,
        'ProductOfferObj':ProductOfferObj
    }
    return render(request,'adminside/Edit_ProductOffer.html',context)



# # --------------------------- View Product Offers --------------------------- #
def View_ProductOffers(request):
    ProductOfferObj=Productoffer.objects.all()
    paginator=Paginator(ProductOfferObj,per_page=2)
    page_number=request.GET.get('page')
    ProductOfferObjfinal=paginator.get_page(page_number)
    totalpage=ProductOfferObjfinal.paginator.num_pages
    context={
        'ProductOffer':ProductOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'adminside/View_ProductOffer.html',context)


# -------------------------- Delete A Product Offer ------------------------- #
def Delete_ProductOffer(request,id):
    toDelete_ProductOffer=Productoffer.objects.get(id=id)
    
    toDelete_ProductOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_ProductOffers)

# ---------------------------- Block ProductOffer --------------------------- #
def Block_ProductOffer(request,id):
    toBlock_ProductOffer=Productoffer.objects.get(id=id)
    toBlock_ProductOffer.is_active=False
    toBlock_ProductOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_ProductOffers)

# --------------------------- Unblock ProductOffer -------------------------- #
def UnBlock_ProductOffer(request,id):
    toUnBlock_ProductOffer=Productoffer.objects.get(id=id)
    toUnBlock_ProductOffer.is_active=True
    toUnBlock_ProductOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_ProductOffers)    


# ------------------------------ Sales Report------------------------------ #
# --------------------------- sales report-------------------------- #

def salesreport(request):
    salesreport = Order.objects.all().order_by('id')
    
    if request.method  == 'POST':
        search = request.POST["salesreport_search"]
        salesreports = Order.objects.filter(order_id__contains = search)
        context = {
            'salesreport':salesreports
        }
        return render (request,"adminside/salesreport.html",context)
   
    context = {
            'salesreport':salesreport
        }
    return render (request,"adminside/salesreport.html",context)


# --------------------------- date-------------------------- #

def date_range(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        if len(fromdate)>0 and len(todate)> 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]

            salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]) )

            context = {
                'salesreport':salesreport,
            }

            return render(request,'adminside/salesreport.html',context)

        else:
            salesreport = Order.objects.all()
            context = {
                'salesreport': salesreport ,

             }
            


    return render (request,"adminside/salesreport.html",context)
        
# --------------------------- monthly report-------------------------- #


def monthly_report(request,date):
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,28]

    salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'adminside/salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'adminside/salesreport.html')

# --------------------------- yearly sales report-------------------------- #

def yearly_report(request,date):
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]

    salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'adminside/salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'adminside/salesreport.html')    