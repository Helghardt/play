from django.contrib import admin

# Register your models here.
from escrow.models import Escrow


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class EscrowAdmin(CustomModelAdmin):
    pass

admin.site.register(Escrow, EscrowAdmin)