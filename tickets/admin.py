from django.contrib import admin
from tickets.models import Event, Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', "get_event_name", "email")
    search_fields = ('event__name', "event_id")
    raw_id_fields = ("event",)

    @admin.display(description="Название мероприятия")
    def get_event_name(self, obj):
        return obj.event.name if obj.event else "-"


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', "name", 'event_date')
    search_fields = ('name', "event_date")


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
