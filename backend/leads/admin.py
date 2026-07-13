from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from leads.models import Lead

@admin.register(Lead)
class LeadAdmin(SimpleHistoryAdmin):
    # define las columnas que se verán en la lista general de Leads
    list_display = ["title", "created_at"] 
