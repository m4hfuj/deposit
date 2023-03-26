import random
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Box, Client, Transaction, Employee, Visitation



def show_home(request):
    return render(request, 'home.html')



def show_clients(request):
    clients = Client.objects.raw("SELECT * FROM main_client ORDER BY client_id")
    ages = []
    for client in clients:
        age = (date.today() - client.birthdate) // timedelta(days=365.2425)
        ages.append(age)

    return render(request, 'clients/clients.html', {
        "clients": clients,
        "clients_ages": zip(clients, ages),
    })



def show_client_dashboard(request, pk):
    client = Client.objects.get(id=pk)
    trans = client.transaction_set.all().order_by('box__box_number')
    # Calculation of box-rents 
    box_rents = [] 
    expiry_dates = []
    transactions = []
    for t in trans:
        if t.box.available == False and t.islast == True:
            box = Box.objects.get(pk = t.box_id)
            if (box.size == 'lg'):
                billing = 200.00
            elif (box.size == 'md'):
                billing = 150.00
            else:
                billing = 100.00
            transactions.append(t)
            box_rents.append(billing)
            expiry_dates.append(t.registration_date + relativedelta(months=t.rental_duration))
    # Request: POST
    if request.method == 'POST':
        # Get Data
        transaction_id = request.POST.get('transaction-id')
        box_id = request.POST.get('box-id')
        box = Box.objects.get(id=box_id)
        # Change Box Availability to True
        box.available = True
        box.save()
        # Redirect the user to a success page
        return redirect('client-dashboard', pk=client.pk)

    context = {'client': client, 'transactions': transactions, 'boxes': zip(transactions, box_rents, expiry_dates)}
    return render(request, 'clients/client-dashboard.html', context)



# This is creating transactions entry
def register_box(request, pk):
    client = Client.objects.get(id=pk)
    boxes = Box.objects.filter(available=True)
    # box-rent Calculation
    box_rents = []
    for box in boxes:
        if 'C' in box.box_number:
            box_rents.append(100)
        elif 'A' in box.box_number:
            box_rents.append(200)
        else:
            box_rents.append(150)
    # Request: POST
    if request.method == 'POST':
        # Get the data from the form
        box_number = request.POST.get('box-number')
        rental_duration = request.POST.get('rental-duration')
        box = Box.objects.get(box_number=box_number)
        # Making prev_transaction islast = False
        try:
            prev_transaction = get_object_or_404(Transaction, client=client, box=box, islast=True)
            prev_transaction.islast = False
            prev_transaction.save()
        except:
            pass

        # Calculate Registration Date
        x = datetime.datetime.now()
        reg_date = x.strftime("%Y-%m-%d")
        # Calculate Billing Amount
        if (box.size == 'lg'):
            billing = 200.00
        elif (box.size == 'md'):
            billing = 150.00
        else:
            billing = 100.00

        total_billing = str( float(billing) * float(rental_duration) )
        # Create a new_object with the data
        new_object = Transaction(
            client = client, 
            box = box, 
            registration_date = reg_date, 
            rental_duration = rental_duration, 
            billing_amount = total_billing,
            islast = True
        )
        new_object.save()
        # Change Box Availability to False
        box.available = False
        box.save()
        # Redirect the user to a success page
        return redirect('client-dashboard', pk=client.pk)

    context = {
        'client': client, 
        'boxes': boxes,
        'box_rents': box_rents,
    }
    return render(request, 'clients/register-box.html', context)



def visitations(request, pk):
    client = Client.objects.get(pk=pk)
    visits = Visitation.objects.filter(client = client).order_by('visit_date')

    return render(request, 'clients/visitations.html', {
        'client': client,
        'visits': visits,
    })



def add_visitation(request, pk):
    client = Client.objects.get(pk=pk)
    # transactions = Transaction.objects.filter(client = client)
    boxes = Box.objects.filter(transaction__client = client, available = False).distinct()

    if request.method == 'POST':
        # Get Data
        # client_name = request.POST.get('client-name')
        box_number = request.POST.get('box-number')
        box = Box.objects.get(box_number = box_number)
        visit_date = request.POST.get('visit-date')
        check_in = request.POST.get('check-in')
        check_out = request.POST.get('check-out')
        # add new_object
        new_object = Visitation(
            client = client,
            box = box,
            visit_date = visit_date,
            check_in = check_in,
            check_out = check_out,
        )
        new_object.save()
        return redirect('visitations', pk=client.pk)

    return render(request, 'clients/add-visitation.html', {
        'client': client,
        'boxes': boxes,
    })



def remove_box(request, pk):
    client = Client.objects.get(pk=pk)
    # transactions = client.transaction_set.all()
    transactions = Transaction.objects.filter(client = client)
    # Calculation of Box Rents and Rental Duration
    box_rents = []
    expiry_dates = []
    for t in transactions:
        box = Box.objects.get(pk=t.box_id)
        if (box.size == 'lg'):
            billing = 200.00
        elif (box.size == 'md'):
            billing = 150.00
        else:
            billing = 100.00
        box_rents.append(billing)
        expiry_dates.append(t.registration_date + relativedelta(months=t.rental_duration))
    # Request: POST
    if request.method == 'POST':
        # Get Data
        transaction_id = request.POST.get('transaction-id')
        box_id = request.POST.get('box-id')
        box = Box.objects.get(id=box_id)
        # Change Box Availability to True
        box.available = True
        box.save()
        # Redirect the user to a success page
        return redirect('clients/client-dashboard', pk=client.pk)

    context = {'client': client, 'boxes': zip(transactions, box_rents, expiry_dates)}
    return render(request, 'clients/remove-box.html', context)



def register_client(request):
    # employee = Employee.objects.get(employee_id=102)
    if request.method == 'POST':
        # Get Data
        name = request.POST.get('name')
        pic_url = request.POST.get('pic')
        firm_name = request.POST.get('firm-name')
        firm_location = request.POST.get('firm-location')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        birthdate = request.POST.get('birthday')
        hair_color = request.POST.get('hair-color')
        eye_color = request.POST.get('eye-color')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        # Generate a random 4-digit number
        num = random.randint(100000, 999999)
        client_id = num
        # new Client Object
        new_client = Client(
            client_id = client_id,
            name = name,
            pic_url = pic_url,
            firm_name = firm_name,
            firm_location = firm_location,
            email = email,
            address = address,
            phone = phone,
            birthdate = birthdate,
            hair_color = hair_color,
            eye_color = eye_color,
            height = height,
            weight = weight,
        )
        new_client.save()
        return redirect('clients')

    return render(request, 'clients/register-client.html')
    # return render(request, 'contact.html', {'form': form})
        


def client_profile(request, pk):
    client = Client.objects.get(id=pk)
    f = int(client.height) / 12
    i = int(client.height) % 12
    return render(request, 'clients/client-profile.html', {
        'client': client,
        'f': int(f),
        'i': int(i),
    })



def confirm_delete(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        # Get Data
        client_pk = request.POST.get('client-pk')
        client = Client.objects.get(id=client_pk)
        client.delete()
        return redirect('clients')

    context = {'client': client}
    return render(request, 'confirm-delete.html', context)



def show_boxes(request):
    boxes = Box.objects.raw('SELECT * FROM main_box ORDER BY box_number')
    # Calculation box-rent, tr-color
    box_rents = []
    tr_colors = []
    for box in boxes:
        if 'C' in box.box_number:
            box_rents.append(100)
        elif 'A' in box.box_number:
            box_rents.append(200)
        else:
            box_rents.append(150)
        if box.available == True:
            tr_colors.append('-success')
        else:
            tr_colors.append('-danger')

    # Calculate Expiry Date
    today = date.today()  # get today's date
    rental_duration = 4  # rental duration in months
    expiry_date = today + timedelta(days=rental_duration*30)  # add 4 months to today's date

    context = {"boxes": zip(boxes, box_rents, tr_colors)}
    return render(request, 'boxes/boxes.html', context)



def box_history(request, pk):
    box = Box.objects.get(pk=pk)
    transactions = Transaction.objects.filter(box = box)
    return render(request, 'boxes/box-history.html', {
        'box': box,
        'transactions': transactions,
    })