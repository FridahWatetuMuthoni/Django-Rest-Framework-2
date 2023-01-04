from django.urls import path
from . import views

urlpatterns = [
    # This url handles get request of all customers, and a post request
    path('customers/', views.CustomerView.as_view(), name='customers'),
    # This url handles the get request of a single customer, put request and delete request
    path('customers/<str:pk>/', views.CustomerDetailView.as_view(),
         name='customer_detail')
]
