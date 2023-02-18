from django.shortcuts import render, redirect
from .forms import PizzaForm
from .models import Pizza
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request, 'pizza/index.html')

class HomeView(TemplateView):
    template_name = 'pizza/index.html'

@login_required()
def make_order(request):
    form = PizzaForm()

    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            pizza.user = request.user
            pizza.save()
            messages.success(request, "Your order is on the way")
            return redirect('home')

    context = {
        "form" : form
    }

    return render(request, 'pizza/order.html', context)

class PizzaOrder(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/order.html' # default templatename for CreateView 'pizza/pizza_form.html'
    success_url = reverse_lazy('my_order')
    success_message = "Your order is on the way!"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


@login_required()
def list_order(request):
    orders = Pizza.objects.filter(user=request.user)

    context = {
        "data" : orders
    }

    return render(request, 'pizza/list_orders.html', context)

class ListPizzaOrders(LoginRequiredMixin, ListView):
    model = Pizza
    context_object_name = 'data' # default name 'object_list'
    template_name = 'pizza/list_orders.html' # default templatename 'pizza/pizza_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    # def get_context_data(self, **kwargs):
    #     test = super().get_context_data(**kwargs)
    #     data = test.get('data')
    #     test["data"] = data.filter(user=self.request.user)
    #     return  test


@login_required()
def update_order(request, id):
    pizza = Pizza.objects.get(id=id)

    if pizza.user != request.user:
        messages.error(request, 'Permission denied')
        return redirect('home')

    if pizza.is_order_expired():
        messages.error(request, 'Time passed for making an update')
        return redirect('my_order')

    # if timezone.now() > pizza.created + "2hrs":
    #     messages.error('Time passed for making an update')
    #     return redirect('my_order')

    form = PizzaForm(instance=pizza)

    if request.method == 'POST':
        form = PizzaForm(request.POST, instance=pizza)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated!')
            return redirect('my_order')

    context = {
        "form": form,
        "id": id
    }

    return render(request, 'pizza/order_update.html', context)

class PizzaOrderUpdate(LoginRequiredMixin, UpdateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/order_update.html'
    success_url = reverse_lazy('my_order')
    pk_url_kwarg = 'id' # default is pk
    success_message = "Your order is updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.get_object().id
        context["id"] = id
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user:
            messages.error(request, 'Permission denied')
            return redirect('home')

        if self.object.is_order_expired():
            messages.error(request, 'Time passed for making an update')
            return redirect('my_order')

        return super().get(request, *args, **kwargs)

@login_required()
def delete_order(request, id):
    pizza = Pizza.objects.get(id=id)

    if pizza.user != request.user:
        messages.error(request, 'Permission denied')
        return redirect('home')

    if request.method == 'POST':
        pizza.delete()
        messages.success(request, 'Order is canceled')
        return redirect('home')

    return render(request, 'pizza/order_delete.html')

class PizzaOrderDelete(LoginRequiredMixin, DeleteView):
    model = Pizza
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('my_order')
    template_name = 'pizza/order_delete.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user:
            messages.error(request, 'Permission denied')
            return redirect('home')

        if self.object.is_order_expired():
            messages.error(request, 'Time passed for cancelling')
            return redirect('my_order')

        return super().get(request, *args, **kwargs)
