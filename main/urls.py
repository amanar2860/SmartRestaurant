from django.conf.urls import url
from django.urls import path
from . import views
from .views import (
    MenuListView,
    menuDetail,
    add_to_cart,
    get_cart_items,
    order_item,
    CartDeleteView,
    order_details,
    admin_view,
    genrate_qrcode,
    item_list,
    pending_orders,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    update_status,
    add_reviews,
    aboutus_view,
    home, CategoryCreateView, TableOrdersCreateView, CategoryUpdateView, FeedbackCreateView)

app_name = "main"

urlpatterns = [
    path('', MenuListView.as_view(), name='index'),
    #path('home/', home.as_view(), name='home'),
    path('home/', views.home, name='home'),
    path('home/<catid>', views.home_filter, name='home_filter'),
    path('dishes/<slug>', views.menuDetail, name='dishes'),
    path('category_list/', views.category_list, name='category_list'),
    path('category/new/', CategoryCreateView.as_view(), name='category-create'),
    path('category-update/<slug>/', CategoryUpdateView.as_view(), name='category-update'),

    path('item_list/', views.item_list, name='item_list'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('table_booking/new/', TableOrdersCreateView.as_view(), name='tableorder-create'),
    path('item-update/<slug>/', ItemUpdateView.as_view(), name='item-update'),
    path('item-delete/<slug>/', ItemDeleteView.as_view(), name='item-delete'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/', CartDeleteView.as_view(), name='remove-from-cart'),
    path('ordered/', views.order_item, name='ordered'),
    path('ordered/<paymodeIsDonated>', views.order_item, name='ordered'),
    path('payment_view/', views.payment_view, name='payment_view'),
    path('order_details/', views.order_details, name='order_details'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('genrate_qrcode/', views.genrate_qrcode, name='genrate_qrcode'),
    path('donate/', views.donate, name='donate'),
    path('paymentchoise/', views.paymentchoise, name='paymentchoise'),
    path('scan_qrcode/', views.scan_qrcode, name='scan_qrcode'),
    path('table-reserv-success/', views.tablesuccess, name='table-booking-successful'),
    path('order-success/', views.ordersuccess, name='ordersuccess'),

    path('aboutus_view/', views.aboutus_view, name='aboutus_view'),
    path('contactus_view/', views.contactus_view, name='contactus_view'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<int:pk>', views.update_status, name='update_status'),
    path('postReview', views.add_reviews, name='add_reviews'),

    path('feedback_list/', views.feedback_list, name='feedback_list'),
    path('feedback/new/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('add_session_value/<tno>/', views.add_session_value, name='add_session_value'),

]
