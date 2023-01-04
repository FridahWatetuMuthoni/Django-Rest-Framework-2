from django.contrib import admin
from .models import User, Customer

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_name', 'gender',
                    'user', 'created', 'updated', 'status')
    readonly_fields = ('created',)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


admin.site.register(Customer, CustomerAdmin)
admin.site.register(User)
