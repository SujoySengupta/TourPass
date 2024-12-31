from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
import razorpay.errors
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import razorpay
from django.conf import settings
from django.core.mail import send_mail


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
def book_ticket_view(request, museum_id):
    if request.method == 'POST':
        museum = get_object_or_404(Museum, pk=museum_id)
        timeslot_id = request.POST.get('timeslot')  # Assuming you're sending timeslot_id from the form
        quantity = int(request.POST.get('quantity', 1))

        # Get the timeslot
        timeslot = get_object_or_404(TimeSlot, pk=timeslot_id)

        # Create booking with pending status
        booking = Booking.objects.create(
            user=request.user,
            museum=museum,
            timeslot=timeslot,  # Use timeslot instead of visit_date
            quantity=quantity,
            status='pending'
        )

        try:
            return redirect('payment_page', booking_id=booking.id)
        except Exception as e:
            booking.delete()
            return HttpResponseBadRequest('Payment initialization failed')
            
    return HttpResponseBadRequest('invalid request.')

# @login_required
def payment_view(request,booking_id):
    booking = get_object_or_404(
        Booking, 
        pk=booking_id, 
        user=request.user, 
        status='pending'
    )
    
    # Initialize razorpay cilent
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    
    # Convert INR to paise
    amount = int(booking.total_price*100)

    # Create a Razorpay order
    order_data = {
        'amount':amount,
        'currency':'INR',
        'payment_capture':1,
    }
    razorpay_order = client.order.create(data=order_data)

    # Store the order_id in the booking so we can verify payment later
    booking.razorpay_order_id = razorpay_order.get('id')
    booking.save()
    context = {
        'booking':booking,
        'order_id':razorpay_order['id'],
        'order_amount':amount,
        'api_key':settings.RAZORPAY_KEY_ID,
    }
    return render(request,'payment.html',context)

@login_required
def payment_succes_view(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    if not (payment_id and order_id and signature):
        return render(request, 'payment_failed.html', {'message': 'Payment parameters are missing.'})
    
    booking = get_object_or_404(Booking, razorpay_order_id=order_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Fix the typo in 'razorpay_payment_id'
    params_dict = {
        'razorpay_payment_id': payment_id,  # Fix typo here
        'razorpay_order_id': order_id,
        'razorpay_signature': signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        booking.razorpay_payment_id = payment_id
        booking.razorpay_signature = signature
        booking.status = 'confirmed'
        booking.save()
        return render(request, 'payment_success.html', {'booking': booking})
    except razorpay.errors.SignatureVerificationError:
        return render(request, 'payment_failed.html', 
                     {'message': 'Payment verification failed: Please contact support.'})