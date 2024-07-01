import json
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import DeleteView
from cart.forms import CartAddProductForm
from rest_framework import viewsets
from .serializers import ProductSerializer

from .models import Product

def contact(request):
    return render(request, 'myapp/contact.html')

def index(request):
    page_obj = items = Product.objects.all()

    item_name = request.GET.get("search")
    if item_name != "" and item_name is not None:
        page_obj = items.filter(name__icontains=item_name)

    paginator = Paginator(page_obj, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "myapp/index.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "myapp/index.html"
    context_object_name = "items"
    paginate_by = 6


# def indexItem(request, my_id):
#     item = Product.objects.get(id=my_id)
#     context = {"item": item}
#     return render(request, "myapp/detail.html", context=context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "myapp/detail.html"
    context_object_name = "item"
    pk_url_kwarg = "pk"
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.get_object()
        cart_product_form = CartAddProductForm()
        context["product"] = product
        context["cart_product_form"] = cart_product_form
        context["stripe_publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
    def is_admin(request):
        if request.user.groups.filter(name="администраторы").exists() == True:
            return render(request, True)
        else:
            return render(request, False)


@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES["upload"]
        seller = request.user
        item = Product(
            name=name, price=price, description=description, image=image, seller=seller
        )
        item.save()
    return render(request, "myapp/additem.html")


def update_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get("upload", item.image)
        item.save()
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/updateitem.html", context)


def delete_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/deleteitem.html", context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("myapp:index")



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer