# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # '''This url link lists use in anquira'''
    path('links-list', views.links_list, name="links_list"),
    path('genrate-payment-link', views.genrate_payment_link, name="genrate_payment_link"),
    path('get-payment-link', views.get_payment_link, name="get_payment_link"),
    path('mark-payment-other-source/<slug:row_id>', views.mark_payment_other_source, name="mark_payment_other_source"),


    # path('', views.ap2v_fee_payments, name="ap2v_fee_payments"),
    # path('add-to-cart', views.add_to_cart, name="add_to_cart"),
    path('order-receipt', views.order_receipt, name="order_receipt"),
    path('<slug:uuid>', views.add_to_cart, name="add_to_cart"),
    path('disabled-payment-link/<slug:id>', views.disabled_payment_link, name="disabled_payment_link"),
]
