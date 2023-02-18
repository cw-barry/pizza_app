from django.urls import path
# from .views import home, make_order, list_order, update_order, delete_order
from .views import *

urlpatterns = [
    # path('', home, name="home"),
    path('', HomeView.as_view(), name="home"),
    # path('order/', make_order, name="order"),
    path('order/', PizzaOrder.as_view(), name="order"),
    # path('order/<int:id>/', update_order, name="update_order"),
    path('order/<int:id>/', PizzaOrderUpdate.as_view(), name="update_order"),
    # path('delete/<int:id>/', delete_order, name="delete_order"),
    path('delete/<int:id>/', PizzaOrderDelete.as_view(), name="delete_order"),
    # path('myorder/', list_order, name="my_order"),
    path('myorder/', ListPizzaOrders.as_view(), name="my_order"),
]
