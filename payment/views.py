from enum import unique
from django.http import HttpResponse
from django.shortcuts import redirect, render
# from anquira import payment
import razorpay
from .models import Order_plan_details
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator

# Create your views here.

def ap2v_fee_payments(request):
    # return HttpResponse("ok")
    return render(request, "payments/payment.html")

def add_to_cart(request,uuid):
    ctx={}
    if uuid:
        order_obj = Order_plan_details.objects.filter(payment_uuid=uuid).first()
        if order_obj.is_active == True:
            if order_obj:
            
                if order_obj.razorpay_payment_id and order_obj.razorpay_order_id  and order_obj.razorpay_signature:
                    ctx['order_details'] = order_obj
                    ctx['message'] = "You have already completed your payment. Duplicate receipt."
                    return render(request, 'payments/success.html',ctx)
                else:
                    print("----------------------------")
                    print(order_obj.razerpay_order_obj)
                    ctx['payment'] = {"amount":order_obj.amount,"id":order_obj.order_id}

                    ctx['name']=order_obj.name
                    ctx['email']=order_obj.email
                    ctx['amount']=order_obj.amount
                    ctx['key']=settings.RAZORPAY_KEY
                    ctx['mobile']=order_obj.mobile
                    ctx['ramnt']=int(order_obj.amount)*100
                return render(request, "payments/pay_cart.html",ctx)
            else:
                return render(request, "v4_home/error_course_not_found.html",ctx,status=404)
        else:
            return render(request, "v4_home/error_course_not_found.html",ctx,status=404)
    else:
        return render(request, "v4_home/error_course_not_found.html",ctx,status=404)


@csrf_exempt
def order_receipt(request):
    ctx={}
    if request.method == "POST":
        confirm_data = request.POST
        print("-----------------------------------------------------")
        print(confirm_data)
        order_id = confirm_data['razorpay_order_id']
        if confirm_data['razorpay_order_id'] and confirm_data['razorpay_payment_id'] and confirm_data['razorpay_signature']:
            order_details = Order_plan_details.objects.filter(order_id = order_id).first()
            order_details.razorpay_order_id = confirm_data['razorpay_order_id']
            order_details.razorpay_payment_id = confirm_data['razorpay_payment_id']
            order_details.razorpay_signature = confirm_data['razorpay_signature']
            order_details.payment_status = True
            order_details.save()
            ctx['order_details'] = order_details
            
        return render(request, 'payments/success.html',ctx)
    return render(request, 'payments/failed.html',ctx)

def links_list(request):
    
    name=request.GET.get("name", None)
    mobile=request.GET.get("mobile", None)
    email=request.GET.get("email", None)
    ctx = {}
    # print('asaasp'*100)
    # print(name)
    # print(mobile)
    # print(email)

    if name:
        payment_obj = Order_plan_details.objects.filter(name=name)
    elif mobile:
        payment_obj = Order_plan_details.objects.filter(mobile=mobile)
    elif email:
        payment_obj = Order_plan_details.objects.filter(email=email)
    else:
        payment_obj = Order_plan_details.objects.all().order_by("-id")

    paginator = Paginator(payment_obj, 10)
    page_number = request.GET.get('page')
    try:
        payment_obj = paginator.page(page_number)
    except:
        payment_obj = paginator.page(1)

    ctx['payment_obj']=payment_obj
    return render(request, 'payment-list.html',ctx)

def genrate_payment_link(request):
    ctx={}
    if request.method == "POST":
        name = request.POST.get("name",None)
        fee_title = request.POST.get("fee_title",None)
        email = request.POST.get("email",None)
        mobile = request.POST.get("mobile",None)
        fee = request.POST.get("fee",None)

        if name and email and fee_title and mobile and fee:
            order_amount = int(fee)*100
            order_currency = 'INR'
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY,settings.RAZORPAY_SECERT))
            order_receipt = "AP2V Course Payment"
            notes = {'user': email}
            payment = client.order.create({"amount":order_amount, "currency":order_currency, "receipt":order_receipt, "notes":notes})
            print("----------------------------")
            print(payment)
            ctx['payment'] = payment
            x = Order_plan_details(
                name = name,
                fee_title = fee_title,
                email = email,
                mobile = mobile,
                amount = fee,
                order_id = payment['id'],
                razerpay_order_obj = payment
            )
            x.save()

            unique_uuid = x.payment_uuid
            print(unique_uuid)
            ctx['payment_link'] = settings.BASE_URL+"/pay/"+str(unique_uuid)

            return render(request, "link.html",ctx)

def get_payment_link(request):
    ctx={}
    id = request.GET.get("id",None)
    if id:
        payment_list_obj = Order_plan_details.objects.filter(id=id).first()
        if payment_list_obj:
            print(payment_list_obj.payment_uuid)
            payment_link = settings.BASE_URL+"/pay/"+str(payment_list_obj.payment_uuid)
            ctx['payment_list_obj']=payment_list_obj
            ctx['payment_link']=payment_link
    return render(request, "link.html",ctx)

def mark_payment_other_source(request,row_id):
    payment_row_id = row_id
    print(payment_row_id)
    if payment_row_id:
        Order_plan_details.objects.filter(id=payment_row_id).update(
            received_other_source = True
        )
    return redirect('links_list')



'''
    This Function disabled the payment link, 
    if want to enabled us admin -> [is_active==True] do this.
'''
def disabled_payment_link(request,id):
    # print(id)
    Order_plan_details.objects.filter(id=id).update(
        is_active = False
    )
    return redirect('links_list')