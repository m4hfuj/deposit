from django.contrib import admin
from .models import Employee, Client, Box, Transaction, Visitation

admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Box)
admin.site.register(Transaction)
admin.site.register(Visitation)