from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings
import json
import stripe
from django.views.generic import TemplateView
from django.http import HttpResponseNotFound, JsonResponse
from .cart import Cart
from .forms import CartAddProductForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import OrderDetail
from myapp.models import Product
import stripe


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@csrf_exempt
def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Create the line item for the product
    line_item = {
        "price_data": {
            "currency": "usd",
            "product_data": {
                "name": product.name,
            },
            "unit_amount": int(product.price * 100),  # Price in cents for Stripe
        },
        "quantity": 1,
    }

    # Create a Stripe checkout session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[line_item],
        mode="payment",
        success_url = request.build_absolute_uri(reverse('cart:create_checkout_session', kwargs={'product_id': product.id}))
    )

    return JsonResponse({"sessionId": checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "myapp/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "myapp/payment_failed.html"

