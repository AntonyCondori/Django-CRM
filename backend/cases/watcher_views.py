"""Watch / unwatch / list-watchers REST endpoints.

URL surface (mounted under /api/cases/):
    POST   /<id>/watch/      — subscribe the requesting profile (idempotent)
    DELETE /<id>/watch/      — unsubscribe
    GET    /<id>/watchers/   — list everyone watching the case
    GET    /watching/        — cases the current profile watches

Authorisation: a user who can see the case can also watch it. Cases visible
to a user are computed exactly as in `CaseListView.get_queryset` — admins
see everything; non-admins see cases they created OR are assigned to OR
already watch (so a watcher who was un-assigned can still unsubscribe).
"""

from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cases.models import Case, CaseWatcher
from cases.serializer import CaseSerializer

def _visible_cases_qs(profile):
    """Cases the requester is allowed to interact with.

    Mirrors `CaseListView.get_queryset` and adds the watchers allowance from
    `docs/cases/tier2/watchers-mentions.md` "Watcher who loses access".
    """
    qs = Case.objects.filter(org=profile.org)
    if profile.role == "ADMIN" or getattr(profile, "is_admin", False):
        return qs
    return qs.filter(
        Q(created_by=profile.user)
        | Q(assigned_to=profile)
        | Q(watchers=profile)
    ).distinct()


@extend_schema(exclude=True)
class WatchView(APIView):
    """POST/DELETE /api/cases/<pk>/watch/"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: inline_serializer(
            name="WatchResponse",
            fields={
                "watching": serializers.BooleanField(),
                "subscribed_via": serializers.CharField()
            }
        )},
        description="Agrega al usuario actual a la lista de observadores del caso."
    )
    def post(self, request, pk, *args, **kwargs):
        case = get_object_or_404(_visible_cases_qs(request.profile), pk=pk)
        try:
            obj, created = CaseWatcher.objects.get_or_create(
                case=case,
                profile=request.profile,
                defaults={
                    "org": case.org,
                    "subscribed_via": "manual",
                },
            )
        except IntegrityError:
            obj = CaseWatcher.objects.get(case=case, profile=request.profile)
            created = False
        return Response(
            {"watching": True, "subscribed_via": obj.subscribed_via},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @extend_schema(
        responses={204: None},
        description="Remueve al usuario actual de la lista de observadores."
    )
    def delete(self, request, pk, *args, **kwargs):
        case = get_object_or_404(_visible_cases_qs(request.profile), pk=pk)
        CaseWatcher.objects.filter(case=case, profile=request.profile).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchersListView(APIView):
    """GET /api/cases/<pk>/watchers/"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: inline_serializer(
            name="WatchersListResponse",
            fields={
                "count": serializers.IntegerField(),
                "watchers": serializers.ListField(child=serializers.JSONField())
            }
        )},
        description="Obtiene la lista de todos los agentes que observan este caso."
    )
    def get(self, request, pk, *args, **kwargs):
        case = get_object_or_404(_visible_cases_qs(request.profile), pk=pk)
        rows = (
            CaseWatcher.objects.filter(case=case)
            .select_related("profile__user")
            .order_by("created_at")
        )
        watchers = [
            {
                "id": str(row.id),
                "profile_id": str(row.profile_id),
                "user_id": str(row.profile.user_id) if row.profile.user_id else None,
                "name": (row.profile.user.email if row.profile.user else "") or "",
                "email": row.profile.user.email if row.profile.user else "",
                "subscribed_via": row.subscribed_via,
                "created_at": row.created_at,
            }
            for row in rows
        ]
        return Response({"watchers": watchers, "count": len(watchers)})


class WatchingListView(APIView):
    """GET /api/cases/watching/

    Returns the list of cases the current profile watches. Lightweight
    payload — the full case detail is fetched separately when the user opens
    one. Reusing `Case.serializer.CaseSerializer` for parity with the main
    list endpoint.
    """

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: inline_serializer(
            name="WatchingListResponse",
            fields={
                "count": serializers.IntegerField(),
                "cases": CaseSerializer(many=True)
            }
        )},
        description="Retorna la lista de casos que el perfil del usuario actual está observando."
    )
    def get(self, request, *args, **kwargs):
        from cases.serializer import CaseSerializer

        cases = (
            Case.objects.filter(
                org=request.profile.org, watchers=request.profile
            )
            .order_by("-created_at")
            .distinct()
        )
        return Response(
            {
                "cases": CaseSerializer(cases, many=True).data,
                "count": cases.count(),
            }
        )
