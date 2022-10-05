from django.urls import path
from .import views

urlpatterns = [
    path('confirmpayment',views.confirmpayment,name='confirmpayment') , 
    path('placecod',views.placecod,name='placecod') ,
    path('success/',views.razorpay_sucess,name='success/'),
    path('paypal',views.paypal,name='paypal'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    # path('checkdout',views.checkout,name='checkout'),

]