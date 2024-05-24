from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegistrationForm
from django.forms import formset_factory
from .forms import RoommateIDForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from api.models import Roomie


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_roomie = form.save()
            # After saving, you can redirect or print form data
            request.session['number_of_roommates'] = form.cleaned_data['number_of_roommates']
            request.session['name'] = form.cleaned_data['name']
            request.session['roomie_id'] = new_roomie.roomie_id
            
            # Prepare and send the email
            subject = 'Welcome, new Roomie!'
            message = f'Hello {form.cleaned_data["name"]}, you have been registered with Roomie ID: {new_roomie.roomie_id}.'
            from_email = 'ayeshahussainshaik@gmail.com'
            recipient_list = [form.cleaned_data['email']]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('http://127.0.0.1:8000/RoomieVal')

        else:
            form = RegistrationForm()
            print("Form data not valide:", form.errors)
            return render(request, 'frontend/Registration.html', {'form': form})
    else:
        form = RegistrationForm()
        print("Form data:", form.data)
    return render(request, 'frontend/Registration.html', {'form': form})

def RoomieVal(request):
    current_roomie_id = request.session.get('roomie_id')
    try:
        current_roomie = Roomie.objects.get(pk=current_roomie_id)
    except Roomie.DoesNotExist:
        return redirect('login')
    
    number_of_roommates = request.session.get('number_of_roommates', 0)
    RoommateFormSet = formset_factory(RoommateIDForm, extra=int(number_of_roommates))

    if request.method == 'POST':
        formset = RoommateFormSet(request.POST)
        if formset.is_valid():
            roommate_ids = [current_roomie_id]  # Start list with the current user's ID
            for form in formset:
                roommate_id = form.cleaned_data.get('roommate_id')
                if roommate_id and Roomie.objects.filter(roomie_id=roommate_id).exists():
                    roommate_ids.append(roommate_id)
                else:
                    form.add_error('roommate_id', f'Roommate ID {roommate_id} does not exist')

            # Update roommate IDs for all roommates involved
            for rid in roommate_ids:
                roommate = Roomie.objects.get(roomie_id=rid)
                roommate.roommate_ids = roommate_ids  # Update all roommate IDs to include each other
                roommate.save()

            # Send confirmation emails to all roommates
            subject = 'Roommate Validation Completed'
            message = f'Hello, your Roomie validation is complete. Your roommate IDs are: {roommate_ids}.'
            from_email = 'ayeshahussainshaik@gmail.com'
            recipient_list = [roomie.email for roomie in Roomie.objects.filter(roomie_id__in=roommate_ids)]

            send_mail(subject, message, from_email, recipient_list)

            # Redirect to success page or next action
            return redirect('http://127.0.0.1:8000/RoomieVal')  # Change 'success_page' to your actual success URL
        else:
            print("Validation failed:", formset.errors)
    else:
        formset = RoommateFormSet()

    return render(request, 'frontend/RoomieVal.html', {'formset': formset})


def index(request, *args, **kwargs):
    return render(request, 'frontend/Login.html')

def login(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("Form pass:", password)
            print("Form email:", email)
            try:
                roomie = Roomie.objects.get(email=email)
                if roomie.check_password(password):
                    # Assume you have a way to handle login sessions
                    request.session['roomie_id'] = roomie.roomie_id
                    return redirect('http://127.0.0.1:8000/Login')  # Redirect to a success page
                else:
                    form.add_error(None, 'Invalid credentials')
            except Roomie.DoesNotExist:
                form.add_error(None, 'Invalid credentials')
  # Add non-field error
    else:
        form = LoginForm()

    return render(request, 'frontend/login.html', {'form': form})

def homepage(request, *args, **kwargs):
    return render(request, 'frontend/Homepage.html')
def calendar(request, *args, **kwargs):
    return render(request, 'frontend/Calendar.html')
