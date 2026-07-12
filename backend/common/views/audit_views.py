from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from common.permissions import HasOrgContext
from django.apps import apps
from django.shortcuts import get_object_or_404
from itertools import chain

class GlobalAuditListView(APIView):
    """
    Endpoint unificado para el panel general de auditoría.
    Mezcla y ordena cronológicamente los cambios de múltiples módulos.
    """
    permission_classes = (IsAuthenticated, HasOrgContext)

    def get(self, request, *args, **kwargs):
        org = request.profile.org
        limit = int(request.query_params.get('limit', 50))

        # Cargamos los modelos de cada aplicación
        Lead = apps.get_model('leads', 'Lead')
        Contact = apps.get_model('contacts', 'Contact')
        Account = apps.get_model('accounts', 'Account')
        Opportunity = apps.get_model('opportunity', 'Opportunity')

        # Consultamos los historiales filtrados por organización
        leads_hist = Lead.history.filter(org=org).order_by('-history_date')[:limit]
        contacts_hist = Contact.history.filter(org=org).order_by('-history_date')[:limit]
        accounts_hist = Account.history.filter(org=org).order_by('-history_date')[:limit]
        opps_hist = Opportunity.history.filter(org=org).order_by('-history_date')[:limit]

        # Combinamos y ordenamos cronológicamente
        combined_logs = list(chain(leads_hist, contacts_hist, accounts_hist, opps_hist))
        combined_logs.sort(key=lambda x: x.history_date, reverse=True)
        final_logs = combined_logs[:limit]

        # Importamos e instanciamos el serializador global
        from common.serializer import GlobalAuditLogSerializer
        serializer = GlobalAuditLogSerializer(final_logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
