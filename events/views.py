from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Event, User, Ticket, Review
from .forms import EventForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from haystack.query import SearchQuerySet
from datetime import datetime
from django.contrib import messages
from collections import defaultdict
from django.db.models import Count
from decimal import Decimal
from django.core.serializers import serialize
from .helper import organizer_required, paginate_queryset
from .utils import send_ticket_email

N = 10  #number of events on each page
M = 10  #number of tickets on each page


# views.py



# def purchase_ticket(request):
#     if request.method == 'POST':
#         # Process the purchase (payment, ticket creation, etc.)
#         ticket = Ticket.objects.create(
#             user=request.user,
#             event=some_event,  # Replace with your event logic
#             # other ticket details...
#         )
        
#         # Prepare ticket details message
        
        
#         # Send confirmation email
        
        
#         return redirect('ticket_success')
#     return render(request, 'purchase_ticket.html')

# Create your views here.
def index(request):
    events = Event.objects.all()
    categories = Event.CATEGORY_CHOICES
    category_dict = dict(categories)
    page_obj = paginate_queryset(events, request, N)
    return render(request, "events/index.html", {
        "page_obj" : page_obj,
        "categories" : category_dict.keys
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "events/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "events/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "events/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "events/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "events/register.html")


@login_required
def create(request):
    if request.method == "POST":
        new_event = EventForm(request.POST, request.FILES)
        # print(request.POST)
        # print(request.FILES)
        if new_event.is_valid():
            # print("form is valid")
            new_event = new_event.save(commit=False)
            new_event.organizer = request.user
            request.user.is_organizer = True
            request.user.save()
            new_event.save()
            return HttpResponseRedirect(reverse("index")) #going to change this >> redirect to all events 
        else:
            print("form is invalid")
        print(new_event.errors)
    else:
        new_event = EventForm()
    return render(request, "events/create.html",{
        "form" : new_event
    })
    
def event_view(request, event_id):
    event = get_object_or_404(Event, id = event_id)
    return render(request, "events/event.html", {
        "event" : event
    })
 
@login_required   
def buy_ticket_view(request, event_id):
    if request.method=="POST":
        event_obj = get_object_or_404(Event, id=event_id)
        quantity = int(request.POST.get("quantity"))
        
        if event_obj.is_sold_out():
            messages.warning(request, f"Sold Out! No More Tickets Available")
        elif quantity > event_obj.tickets_remaining():
            messages.warning(request, f"Requested ticket quantity exceeds available tickets. Only {event_obj.tickets_remaining()} tickets are remaining.")
        elif not event_obj.status == "active":
            messages.warning(request, f"Sorry. this Event's date has Passed.")
        else:    
            ticket_bought =  Ticket.objects.create(
                    event = event_obj,
                    attender = request.user,
                    quantity = quantity
                )
            total_price = int(quantity) * event_obj.price
            if event_obj.tickets_remaining == 0:
                event_obj.is_sold_out = True
                event_obj.status = "sold_out"
            messages.success(request, f"ticket was purchased successfully.")
            return render(request, "events/reciept.html", {
                "ticket_bought" : ticket_bought,
                "total_price" : total_price
            })
            
            ticket_details = f"Event: {ticket.event.name}\nDate: {ticket.event.date}\n"
            send_ticket_email(request.user.email, ticket_details)
       
    return HttpResponseRedirect(reverse("event", args=(event_id,) )) 


def search_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            query = data.get('search_keyword', '') 
            category = data.get('category', '') 
            start_date = data.get('start_date', '') 
            end_date = data.get('end_date', '')  
            min_price = data.get('min_price', '') 
            max_price = data.get('max_price', '') 
            location = data.get('location', '')
            
            # print(f"Received data search keyword: {query}, category: {category} date: from {start_date} to {end_date}")
            
            search_results = Event.objects.all()
            # print(search_results)
            if query:
                search_results = search_results.filter(title=query)

            # Filter by category
            if category:
                search_results = search_results.filter(category=category)
                
            if location:
                search_results = search_results.filter(location=location)

            # Filter by date range
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                search_results = search_results.filter(date__gte=start_date, date__lte=end_date)

            # Filter by price range
            if min_price and max_price:
                search_results = search_results.filter(price__gte=float(min_price), price__lte=float(max_price))

            # Prepare results for frontend
            results = [
                {
                    'title': result.title,
                    'category': result.category,
                    'date': result.date.strftime('%Y-%m-%d'),
                    'price': str(result.price),
                    'location' : result.location,
                    'image_url' : result.image.url
                }
                for result in search_results
            ]
            # results = serialize('json', search_results)
            
            return JsonResponse({'results': results}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# @login_required
# def organizer_dashboard(request):
#     organizer = request.user
#     events = organizer.events.all().order_by('-date')
    
#     total_tickets_sold = 0
#     for event in events:
#         total_tickets_sold += int(event.tickets_sold())
#         total_revenue = (event.price) * event.tickets_sold()
#         # print(total_tickets_sold)
#         # print(total_revenue)
    
#     return render (request, "events/organizer.html",{
#         "organized_events" : events,
#         "tickets_sold" : total_tickets_sold,
#         "total_revenue" : total_revenue
#     })



@organizer_required
def organizer_dashboard(request):
    organizer = request.user
    events = organizer.events.all().order_by('-date')

    total_tickets_sold = sum(event.tickets_sold() for event in events)
    total_revenue = sum(event.revenue() for event in events)

    # Prepare data for Charts
    sales_data = []
    revenue_data = []
    event_labels = []
    category_data = defaultdict(int)

    for event in events:
        event_labels.append(event.title)
        sales_data.append(event.tickets_sold())
        revenue_data.append(float(event.revenue()))
        category_data[event.category] += event.tickets_sold()  # Aggregate category-wise ticket sales

    category_labels = list(category_data.keys())
    category_sales = list(category_data.values())

    return render(request, "events/organizer.html", {
        "organized_events": events,
        "tickets_sold": total_tickets_sold,
        "total_revenue": float(total_revenue),
        "event_labels": event_labels,
        "sales_data": sales_data,
        "revenue_data": revenue_data,
        "category_labels": category_labels,
        "category_sales": category_sales,
    })


   
@organizer_required
def edit_event_view(request, event_id):
    event = get_object_or_404(Event, id = int(event_id))
    if request.method == "POST":
        action = request.POST.get("action")
        if  action == "delete": 
            event.delete()
            return HttpResponseRedirect(reverse('organizer'))

        event.status = request.POST.get("statusChange")
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return HttpResponseRedirect(reverse('event', args=(event_id,)))
        # print(event_form)
        return render(request, "events/edit.html", {
            "form" : event_form,
            "event" : event
        })
    # print(event)
    else:
        if event.organizer != request.user:
            messages.warning(request, f"Only Organizers can edit Events.")
        event_form = EventForm(instance=event)
        return render(request, "events/edit.html", {
            "form" : event_form,
            "event" : event
        })


@login_required  
def filter_view(request):
    try:
        # data = json.loads(request.body)  # Parse JSON from request body
        filter = request.GET.get('status')
        query = request.GET.get('q')
        
        # search_results = SearchQuerySet().models(Event).all().order_by('-date')
        search_results = Event.objects.all().order_by('-date')
        search_results = search_results.filter(organizer=request.user)
        
        print(request.user)
        # print(search_results)
        if query:
            # print(query)
            search_results = search_results.filter(title=query)
            # print(search_results)
        
            
        if filter == "past":
            search_results = search_results.exclude(status = "active")
        elif filter == "active":
            search_results = search_results.filter(status = "active")
        
        # Prepare results for frontend
        results = [
            {
                'title': result.title,
                'category': result.category,
                'date': result.date.strftime('%Y-%m-%d'),
                'status' : result.status,
                'status_display' : result.get_status_display(),
                'price': str(result.price),
                'location' : result.location,
                'tickets_sold' : str(result.tickets_sold()),
                'revenue' : str(result.revenue()),
            }
            for result in search_results
        ]

        return JsonResponse({'results': results}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
   
@organizer_required
def manage_tickets_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event = event).order_by('-purchased_on')
    page_obj = paginate_queryset(tickets, request, M)
    tickets_json = json.dumps([
        {
            "attender": t.attender.username,
            "event": t.event.title,
            "quantity": t.quantity,
            "purchased_on": t.purchased_on.strftime("%b %d, %Y"),
        }
        for t in page_obj
    ])

    return render(request, "events/tickets.html", {
        "page_obj" : page_obj,
        "event":event,
        "tickets_json": tickets_json
    })
    

# @login_required
# def sort_tickets_view(request):
#     data = json.loads(request.body)
#     tickets = data.get("tickets")
#     # print(tickets)
#     column = request.GET.get("column")
#     order = request.GET.get("order")
    
#     if order == "asc":
#         tickets.order_by(column)
#     elif order == "desc":
#         tickets.order_by(-column)
#     print(tickets)
    