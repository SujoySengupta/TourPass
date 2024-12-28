from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User


# Create your views here.


def museum_list_view(request):
    query = request.GET.get('q')
    if query:
        museums = Museum.objects.filter(Q(name_icontains=query) | Q(location_icontains=query))
    else:
        museums = Museum.objects.all()
    return render(request,'museum_list.html',{'museums':museums,'query':query}) 

def museum_detail_view(request,pk):
    museum = Museum.objects.get(pk=pk)
    time_slots = museum.time_slots.all().order_by('date','time_start')
    return render(request,'museum_detail.html',{'museum':museum,'time_slots':time_slots})

@login_required
def book_ticket_view(request,museum_id):
    if request.method == 'POST':
        museum = get_object_or_404(Museum,pk=museum_id)
        timeslot_id = request.POST.get('timeslot')
        quantity = int(request.POST.get('quantity',1))

        timeslot = get_object_or_404(TimeSlot,pk=timeslot_id,museum=museum)

        if timeslot.remaining_tickets<quantity:
            return HttpResponseBadRequest("Not enough tickets available.")
        
        timeslot.remaining_tickets -= quantity
        timeslot.save()

        booking = Booking.objects.create(user=request.user,museum=museum,timeslot=timeslot,quantity=quantity)

        return redirect('payment_page',booking_id=booking.id)
    return HttpResponseBadRequest('invalid request.')

# @login_required
def payment_view(request,booking_id):
    booking = get_object_or_404(Booking,pk=booking_id,user=request.user,paid=False)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    price_per_ticket = 100
    amount = price_per_ticket*booking.quantity

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data':{'currency':'usd','product_data':{'name':booking.museum.name},'unit_amount':price_per_ticket,},
            'quantity':booking.quantity,
        },],
        mode='payment',
        success_url=request.build_absolute_uri('/payment-success/')+f"?session_id={{CHECHOUT_SESSION_ID}}&booking_id={booking.id}",
        cancel_url=request.build_absolute_uri('/payment-cancel/'),
    )
    return render(request,'payment.html',{'session_id':session.id,'stripe_public_key':settings.STRIPE_PUBLIC_KEY})

# @login_required
def payment_succes_view(request):
    session_id = request.GET.get('session_id')
    booking_id = request.GET.get('booking_id')

    booking = get_object_or_404(Booking,pk=booking_id,user=request.user)
    booking.paid = True
    booking.save()

    subject = 'Museum ticket Booking Confirmation'
    message = f"Hello {booking.user.username},\n\nYour Booking for {booking.museum.name} is confirmed."
    send_mail(subject,message,settings.EMAIL_HOST_USER,[booking.user.email])
    return render(request,'payment_success.html',{'booking':booking})
