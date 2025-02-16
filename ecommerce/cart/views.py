from lib2to3.fixes.fix_input import context
from locale import currency

import razorpay

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart, Payment, Order_details


@login_required
def addtocart(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)
        if p.stock > 0:
            c.quantity += 1
            c.save()
            p.stock -= 1
            p.save()
    except:
        c = Cart.objects.create(user=u, product=p, quantity=1)
        if p.stock > 0:
            c.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cartview')


@login_required
def cartview(request):
    u = request.user
    c = Cart.objects.filter(user=u)
    total = sum(i.quantity * i.product.price for i in c)
    context = {'cart': c, 'total': total}
    return render(request, 'cart.html', context)


@login_required
def cart_decrement(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
            p.stock += 1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cartview')


@login_required
def cart_delete(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)
        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')


def orderform(request):
    if request.method == "POST":
        a = request.POST['a']
        pn = request.POST['ph']  # Ensure this matches the name attribute in the form
        n = request.POST['p']

        u = request.user
        c = Cart.objects.filter(user=u)
        total = sum(i.product.price * i.quantity for i in c)

        client = razorpay.Client(auth=('rzp_test_G1Mjdp01CY6wQg', 'amwkwYSiBpFm48anNMCbrTJJ'))

        response_payment = client.order.create(dict(amount=int(total * 100), currency='INR'))  # Fixed here
        print("Razorpay Order Created: ", response_payment)  # Debugging

        order_id = response_payment['id']
        status = response_payment['status']

        if status == "created":
            p = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()

            for i in c:
                Order_details.objects.create(
                    product=i.product, user=i.user, phone=pn, address=a, pin=n,
                    order_id=order_id, no_of_items=i.quantity
                )

            context = {'payment': response_payment, 'name': u.username}
            return render(request, 'payment.html', context)

    return render(request, 'orderform.html')


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login


@csrf_exempt
def payment_status(request, p):
    user = User.objects.get(username=p)
    login(request, user)

    response = request.POST  # Razorpay response after successful payment
    print("Razorpay Response: ", response)  # Debugging

    param_dict = {
        'razorpay_order_id': response.get('razorpay_order_id', ''),  # Use .get() to avoid KeyError
        'razorpay_payment_id': response.get('razorpay_payment_id', ''),
        'razorpay_signature': response.get('razorpay_signature', ''),
    }

    print("Received Payment Params: ", param_dict)  # Debugging

    client = razorpay.Client(auth=('rzp_test_G1Mjdp01CY6wQg', 'amwkwYSiBpFm48anNMCbrTJJ'))

    try:
        status = client.utility.verify_payment_signature(param_dict)
        print("Verification Status: ", status)

        if status:
            p = Payment.objects.get(order_id=param_dict['razorpay_order_id'])
            p.paid = True
            p.razorpay_payment_id = param_dict['razorpay_payment_id']
            p.save()

            o = Order_details.objects.filter(order_id=param_dict['razorpay_order_id'])
            for i in o:
                i.payment_status = "completed"
                i.save()

            c = Cart.objects.filter(user=user)
            c.delete()
        else:
            print("Payment Signature Verification Failed!")

    except Exception as e:
        print("Error Verifying Payment: ", e)

    return render(request, 'payment_status.html')


@login_required
def orderview(request):
    u = request.user
    o = Order_details.objects.filter(user=u, payment_status="completed")
    context = {'orders': o}
    return render(request, 'orderview.html', context)
