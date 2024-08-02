from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Doctor, Shift, Host, Pet, Illness, Medicine, Appointment

admin.site.register(Doctor)
admin.site.register(Shift)
admin.site.register(Host)
admin.site.register(Pet)
admin.site.register(Illness)
admin.site.register(Medicine)
admin.site.register(Appointment)


class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2', 'email'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

