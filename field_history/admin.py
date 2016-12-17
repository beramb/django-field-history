from django.contrib import admin
from .models import FieldHistory


@admin.register(FieldHistory)
class FieldHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'date_created',  'user')
    list_filter = ('id', 'date_created',  'user')
    search_fields = ('serialized_data', 'object_name', 'user')
    list_per_page = 20
    list_display_links = ('__str__',)
