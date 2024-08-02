from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Shift, Host, Pet, Illness, Medicine, Appointment
from .forms import HostSignUpForm, DoctorLoginForm, HostLoginForm, PetForm, AppointmentForm, ShiftForm, IllnessForm, \
    MedicineForm, AppointmentFormMain


def startpage(request):
    specialization_query = request.GET.get('specialization', None)

    if specialization_query:
        doctors = Doctor.objects.filter(specialization=specialization_query).prefetch_related('shift_set')
    else:
        doctors = Doctor.objects.all().prefetch_related('shift_set')

    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()

    return render(request, 'startpage.html', {
        'doctors': doctors,
        'specializations': specializations,
        'selected_specialization': specialization_query
    })


def host_signup(request):
    if request.method == 'POST':
        form = HostSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = HostSignUpForm()
    return render(request, 'signup.html', {'form': form})


def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('doctor-main')
    else:
        form = DoctorLoginForm()
    return render(request, 'login_doctor.html', {'form': form})


def host_login(request):
    if request.method == 'POST':
        form = HostLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('host-main')
    else:
        form = HostLoginForm()
    return render(request, 'login_host.html', {'form': form})


def host_main(request):
    host = request.user.host
    pets = Pet.objects.filter(owner=host)
    appointments = Appointment.objects.filter(pet__owner=host)

    return render(request, 'host_main.html', {
        'pets': pets,
        'appointments': appointments
    })


@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user.host
            pet.save()
            return redirect('host-main')
    else:
        form = PetForm()
    return render(request, 'add-pet.html', {'form': form})


@login_required
def add_appointment_host(request):
    host = request.user.host

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        form.fields['pet'].queryset = Pet.objects.filter(owner=host)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.host = host
            appointment.save()
            return redirect('host-main')
    else:
        form = AppointmentForm()
        form.fields['pet'].queryset = Pet.objects.filter(owner=host)

    return render(request, 'add-appointment-host.html', {'form': form})


@login_required
def doctor_main(request):
    current_doctor = request.user.doctor

    shifts = Shift.objects.filter(doctor=current_doctor)
    appointments = Appointment.objects.filter(doctor=current_doctor)
    medicines = Medicine.objects.all()
    illnesses = Illness.objects.all()

    context = {
        'shifts': shifts,
        'appointments': appointments,
        'medicines': medicines,
        'illnesses': illnesses,
    }
    return render(request, 'doctor_main.html', context)


@login_required
def change_shifts(request):
    current_doctor = request.user.doctor
    shifts = Shift.objects.filter(doctor=current_doctor)

    if request.method == 'POST':
        if 'delete_shift' in request.POST:
            shift = Shift.objects.get(pk=request.POST['delete_shift'])
            shift.delete()
            return redirect('shifts')
        else:
            form = ShiftForm(request.POST)
            if form.is_valid():
                shift = form.save(commit=False)
                shift.doctor = current_doctor
                shift.save()
                return redirect('shifts')
    else:
        form = ShiftForm()

    context = {
        'shifts': shifts,
        'form': form
    }
    return render(request, 'shifts.html', context)


@login_required()
def change_illness(request):
    if request.method == 'POST':
        if 'delete_illness' in request.POST:
            illness = Illness.objects.get(pk=request.POST['delete_illness'])
            illness.delete()
            return redirect('illnesses')
        else:
            form = IllnessForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('illnesses')
    else:
        form = IllnessForm()

    context = {
        'form': form,
        'illnesses': Illness.objects.all()
    }
    return render(request, 'illnesses.html', context)


@login_required()
def change_medicine(request):
    if request.method == 'POST':
        if 'delete_medicine' in request.POST:
            medicine = Medicine.objects.get(pk=request.POST['delete_medicine'])
            medicine.delete()
            return redirect('medicines')
        else:
            form = MedicineForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('medicines')
    else:
        form = MedicineForm()

    context = {
        'form': form,
        'medicines': Medicine.objects.all()
    }
    return render(request, 'medicines.html', context)


@login_required()
def change_appointment(request):
    if request.method == 'POST':
        if 'delete_appointment' in request.POST:
            appointment = Appointment.objects.get(pk=request.POST['delete_appointment'])
            appointment.delete()
            return redirect('appointment')
        else:
            form = AppointmentFormMain(request.POST)
            if form.is_valid():
                form.save()
                return redirect('appointment')
    else:
        form = AppointmentFormMain()

    context = {
        'form': form,
        'appointments': Appointment.objects.all()
    }
    return render(request, 'appointment.html', context)


@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    if request.method == 'POST':
        form = AppointmentFormMain(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment')
    else:
        form = AppointmentFormMain(instance=appointment)

    context = {
        'form': form,
        'edit': True
    }
    return render(request, 'edit_appointment.html', context)

def logoutt(request):
    logout(request)
    return redirect('index')
