from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.serializer import OrgSettingsSerializer


class OrgSettingsView(APIView):
    """
    API endpoint for org settings (currency, country, locale).

    GET: Returns current org settings
    PATCH: Updates org settings (admin only)
    """

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["Organization Settings"],
        operation_id="common_org_settings_retrieve",
        responses={200: OrgSettingsSerializer},
        description="Obtiene la configuración global actual de la organización (moneda, país, idioma)."
    )
    def get(self, request):
        """Get current organization settings."""
        org = request.profile.org
        serializer = OrgSettingsSerializer(org, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        tags=["Organization Settings"],
        operation_id="common_org_settings_partial_update",
        request=OrgSettingsSerializer,
        responses={
            200: OrgSettingsSerializer,
            400: inline_serializer(
                name="OrgSettingsBadRequestResponse",
                fields={"errors": serializers.JSONField()}
            ),
            403: inline_serializer(
                name="OrgSettingsForbiddenResponse",
                fields={"error": serializers.CharField()}
            )
        },
        description="Permite al administrador actualizar de forma parcial las configuraciones de la organización."
    )
    def patch(self, request):
        """Update organization settings (admin only)."""
        if request.profile.role != "ADMIN" and not request.user.is_superuser:
            return Response(
                {"error": "Only admins can update organization settings"},
                status=status.HTTP_403_FORBIDDEN,
            )

        org = request.profile.org
        serializer = OrgSettingsSerializer(
            org, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
