from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.signinadmin,name='signinadmin'),
    path('adminhome',views.admin_home,name='adminhome'),
    path('adminlogout',views.admin_logout,name='adminlogout'),

    #------------------------- user management ------------------------ #
    path('user_list',views.user_list,name='user_list'),
    path('blockuser/<int:id>/',views.block_user,name='blockuser'),

    #-------------------------product management ------------------------ #
    path('product',views.product,name='product'),
    path('delete/<int:id>/',views.deleteproduct,name='delete'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('addproduct',views.addproduct,name='addproduct'),

    #------------------------- category management ------------------------ #
    path('category',views.categoryList,name='categoryList'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('editcategory/<int:id>/',views.editcategory,name='editcategory'),
    path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),

    # ------------------------------ Brand ----------------------------------#
    path('brand',views.brandlist,name='brandList'),
    path('addbrand',views.addbrand,name='addbrand'),
    path('editbrand/<int:id>/',views.editcategory,name='editbrand'),
    path('deletebrand/<int:id>/',views.deletecategory,name='deletebrand'),

    #------------------------- productlist management ------------------------ #
    path('adminmen',views.adminmen,name='adminmen'),
    path('adminwomen',views.adminwomen,name='adminwomen'),
    path('adminkids',views.adminkids,name='adminkids'),

    #----------------------- order management ------------------------ #
    path("order_management",views.order_management,name="order_management"),
    path("change_status/<int:id>/",views.change_status,name="change_status"),
    path("product_order_management/<int:id>/",views.product_order_management,name="product_order_management"),
    path("product_change_status/<int:id>/",views.product_change_status,name="product_change_status"),

    #------------------------- coupon management ------------------------ #
    path("view_coupon",views.view_coupon,name="view_coupon"),
    path("add_coupon",views.add_coupon,name="add_coupon"),
    path("block_coupon/<int:id>/", views.block_coupon,name="block_coupon"),
    path("delete_coupon/<int:id>/",views.delete_coupon,name="delete_coupon"),

    #------------------------- category offer management ------------------------ #
    path("newcategoryoffer",views.New_CategoryOffer,name="NewCategoryOffer"),
    path("categoryoffers",views.View_CategoryOffers,name="ViewCategoryOffer"),
    path("editcategoryoffers/<int:id>/",views.Edit_CategoryOffer,name="EditCategoryOffer"),
    path("blockcategoryoffers/<int:id>/",views.Block_CategoryOffer,name="BlockCategoryOffer"),
    path("unblockcategoryoffers/<int:id>/",views.UnBlock_CategoryOffer,name="UnBlockCategoryOffer"),
    path("deletecategoryoffers/<int:id>/",views.Delete_CategoryOffer,name="DeleteCategoryOffer"),


#------------------------- Product offer management ------------------------ #
    path("newproductoffer",views.New_ProductOffer,name="NewProductOffer"),
    path("productoffers",views.View_ProductOffers,name="ViewProductOffer"),
    path("editproductoffers/<int:id>/",views.Edit_ProductOffer,name="EditProductOffer"),
    path("blockproductoffers/<int:id>/",views.Block_ProductOffer,name="BlockProductOffer"),
    path("unblockproductoffers/<int:id>/",views.UnBlock_ProductOffer,name="UnBlockProductOffer"),
    path("deleteproductoffers/<int:id>/",views.Delete_ProductOffer,name="DeleteProductOffer"),

#------------------------- sales report ------------------------ #

    path("salesreport",views.salesreport,name="salesreport"),
    path("monthly_report/<int:date>/",views.monthly_report,name="monthly_report"),
    path("yearly_report/<int:date>/",views.yearly_report,name="yearly_report"),
    path("date_range",views.date_range,name="date_range"),
] 