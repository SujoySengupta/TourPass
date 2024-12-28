from django.urls import path
from . import views

urlpatterns = [

    path('', views.museum_list_view, name='museum_list'),
    path('<int:pk>/', views.museum_detail_view, name='museum_detail'),
    path('<int:museum_id>/book/',views.book_ticket_view,name='book_ticket'),
    path('payment/<int:booking_id>/',views.payment_view,name='payment_page'),
    path('payment-success/',views.payment_succes_view,name='payment_success'),
    
]