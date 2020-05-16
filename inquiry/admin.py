from django.contrib import admin
from . models import Inquiry

# Register your models here.


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 25


admin.site.register(Inquiry, InquiryAdmin)

# Register your models here.
