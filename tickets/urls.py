from django.urls import path, include

from tickets.views import TicketsApiView


urlpatterns = [
    path('<int:event_id>/', TicketsApiView.as_view(), name='tickets'),
]

