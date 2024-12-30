from django.db.models import F, Count
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import Ticket, Event


class TicketsApiView(APIView):

    def _authenticate_post_request(self, request, secret: str or None) -> bool:
        if not settings.GETCOURCE_TICKETS_TOKEN or not secret:
            return False
        if secret != settings.GETCOURCE_TICKETS_TOKEN:
            return False
        return True

    def _authenticate_get_request(self, request) -> bool:
        client_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        if client_ip in settings.AVAILABLE_GET_TICKETS_IPS:
            return True
        return False

    def _get_available_event(self, event_id: int) -> Event:
        return Event.objects.filter(id=event_id).annotate(
            available_tickets_count=F('capacity') - Count('ticket')
        ).values('capacity', 'available_tickets_count').first()

    def _create_ticket(self, event_id: int, email: str) -> Ticket:
        return Ticket.objects.create(
            event_id=event_id,
            email=email,
        )

    def get(self, request, *args, **kwargs) -> Response:
        """Возвращает количество доступных билетов на мероприятие"""
        event_id = kwargs.get('event_id')
        if not event_id:
            return Response(status=404, data={'message': 'event_not_found'})

        is_valid_request = self._authenticate_get_request(request)
        if not is_valid_request:
            return Response(
                {"error": "Unauthorized request"},
                status=403
            )

        event = self._get_available_event(event_id=event_id)

        if event:
            event_capacity = event['capacity']
            available_tickets_count = event['available_tickets_count'] if event['available_tickets_count'] >= 0 else 0
        else:
            event_capacity = available_tickets_count = None

        return Response(
            status=200,
            data={
                "event_id": event_id,
                "event_capacity": event_capacity,
                "available_tickets_count": available_tickets_count
            }
        )

    def post(self, request, *args, **kwargs) -> Response:
        """Создает новый билет по интеграции"""
        event_id = kwargs.get('event_id')
        email = request.GET.get('email')
        # Особенность интеграции с getcource - он не может в POST передавать body,
        # поэтому достаем все параметры с GET. Не очень высокая надежность, но хотя бы как-то
        secret = request.GET.get('secret', None)
        if not event_id or not email:
            return Response(
                status=404,
                data={'message': 'some params are empty'},
            )

        is_valid_request = self._authenticate_post_request(request, secret)
        if not is_valid_request:
            return Response(
                {"error": "Unauthorized request"},
                status=403
            )

        ticket = self._create_ticket(event_id=event_id, email=email)

        return Response(
            status=200,
            data={
                "ticket_id": ticket.id,
            },
        )
