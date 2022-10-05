from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path("otpmobile",views.otpmobile,name="otpmobile"),
    path("otp-login/<int:phone_number>/",views.otp_login,name="otpnew"),
    path('menproduct/',views.menproduct,name='men'),
    path('womenproduct',views.womenproduct,name='womenproduct'),
    path('kidsproduct',views.kidsproduct,name='kidsproduct'),
    # ///////////////////////////////////////////////
    path('levis',views.levis,name='levis'),
    path('allensolly',views.allensolly,name='allensolly'),
    path('peter',views.peter,name='peter'),
    path('Miss_Chase',views.Miss_Chase,name='Miss_Chase'),
    path('harpa',views.harpa,name='harpa'),
    path('disney',views.disney,name='disney'),
    path('hopscotch',views.hopscotch,name='hopscotch'),
    path('puma',views.puma,name='puma'),
    path('max',views.max,name='max'),
# ////////////////////////////////////////////////////////
    path('singleproduct/<int:id>/',views.singleproduct,name='singleproduct'),
    path('checkddout',views.checkout,name='checkout'),
    path('addaddress',views.addaddress,name='addaddress'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('useraddress',views.useraddress,name='useraddress'),
    path('addressdelete/<int:id>/',views.addressdelete,name='addressdelete') ,
    path('editaddress/<int:id>/',views.editaddress,name='editaddress') ,
    path('userorder',views.userorder,name='userorder'),
    path('cancelorder/<int:id>/',views.cancelorder,name='cancelorder'),
    path("mensearch",views.mensearch,name="mensearch"),
    path("womensearch",views.womensearch,name="womensearch"),
    path("kidsearch",views.kidsearch,name="kidsearch"),
    # path('order_complete', views.order_complete, name='order_complete'),
    path('product_return/<int:id>/', views.product_return, name='product_return'),
    path('product_order_cancel/<int:id>/', views.product_order_cancel, name='product_order_cancel'),


]