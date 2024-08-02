from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput
from django.utils import timezone

from .models import Host, Pet, Doctor, Appointment, Shift, Illness, Medicine


#SIGN UP HOST
class HostSignUpForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label="Address")
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Phone Number")

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        if commit:
            host = Host(user=user, address=self.cleaned_data['address'], phone_number=self.cleaned_data['phone_number'])
            host.save()
        return user


#LOGIN DOCTOR
class DoctorLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not Doctor.objects.filter(user=user).exists():
            self.add_error(None, ValidationError(
                "Not a doctor",
                code='invalid_login'
            ))

#LOGIN HOST
class HostLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not Host.objects.filter(user=user).exists():
            self.add_error(None, ValidationError(
                "Not a host",
                code='invalid_login'
            ))


#ADD PET
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'birth_date', 'sex']
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


#ADD APPOINTMENT HOST
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'doctor', 'date_time', 'duration', 'notes']
        widgets = {
            'date_time': forms.HiddenInput(attrs={'value': timezone.now().isoformat()}),
        }


#CHANGE DOCOTOR SHIFT
class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['doctor', 'day', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


#Illnesses
class IllnessForm(forms.ModelForm):
    class Meta:
        model = Illness
        fields = ['name', 'description']


#Medicines
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description']


class AppointmentFormMain(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'doctor', 'date_time', 'duration', 'medicines', 'illness', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '00:00'}),
        }

