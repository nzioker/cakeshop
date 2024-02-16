from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

class HomeView(ListView):
    model = Item
    template_name = 'index.html'



class ShopView(ListView):
    model = Item
    template_name = 'shop.html'


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={'object':order}
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


def checkout(request):
    return render(request, "checkout.html")

class CakeView(DetailView):
    model = Item
    template_name = 'cake.html'


@login_required
def add_to_cart(request, slug):
    # get the item you want to add
    item = get_object_or_404(Item, slug=slug)
    # create an orderitem
    orderItem, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    # check whether there is an existing order
    order_qs = Order.objects.filter(user=request.user, ordered=False)

# if an order exists in the orderitem, access the first one and increase its quantity by 1
    if order_qs.exists():
        
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            orderItem.quantity += 1
            orderItem.save()
            messages.info(request, "Order has been succesfully updated")
        else:
            messages.info(request, "Order has been succesfully added")
            order.items.add(orderItem)
    # if not, create a new order and add it to an order item
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(orderItem)
        messages.info(request, "Order has been succesfully created")
    return redirect('cart')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            orderItem = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)[0]
            order.items.remove(orderItem)
            messages.info(request, "Order has been succesfully removed")
            return redirect('cart')
        else:
            messages.info(request, "You do not have an order of this item")
            return redirect('cake', slug=slug)
    # if not, create a new order and add it to an order item
    else:
        messages.info(request, "You dont have this order in your cart.")
        return redirect('cake', slug=slug)
    


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            orderItem = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)[0]
            if orderItem.quantity > 1:
                orderItem.quantity -=1
                orderItem.save()
            else:
                order.items.remove(orderItem)
                messages.info(request, "Your cart is empty")
            
            return redirect('cart')
            
        else:
            messages.info(request, "You do not have an order of this item")
            return redirect('cake')
    # if not, create a new order and add it to an order item
    else:
        messages.info(request, "You dont have this order in your cart.")
        return redirect('cake', slug=slug)
    return redirect('cake', slug=slug)
    
     

    
