from django.contrib import admin
from .models import SupportTicket, TicketMessage

class MessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'subject', 'player', 'category', 'priority', 'status', 'assigned_agent')
    list_filter = ('category', 'status', 'priority')
    inlines = [MessageInline]

admin.site.register(TicketMessage)
