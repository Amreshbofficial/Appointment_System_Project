from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AppointmentForm
from .models import Appointment, Profile, User

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, is_doctor=(role == 'doctor'))
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
        if profile.is_doctor:
            appointments = Appointment.objects.filter(doctor=request.user)
        else:
            appointments = Appointment.objects.filter(patient=request.user)
    except Profile.DoesNotExist:
        appointments = []
    return render(request, 'dashboard.html', {'appointments': appointments})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('dashboard')
    else:
        form = AppointmentForm()
        doctors = User.objects.filter(profile__is_doctor=True)
    return render(request, 'book_appointment.html', {'form': form, 'doctors': doctors})