from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import HasOrgContext
from common.utils import STAGES
from opportunity.models import StageAgingConfig
from opportunity.serializer import StageAgingConfigSerializer
from opportunity.workflow import CLOSED_STAGES, DEFAULT_STAGE_EXPECTED_DAYS


class StageAgingConfigView(APIView):
    permission_classes = (IsAuthenticated, HasOrgContext)

    @extend_schema(
        tags=["Opportunity Stages"],
        operation_id="opportunities_stage_aging_retrieve",
        responses={200: StageAgingConfigSerializer(many=True)},
        description="Obtiene la configuración del tiempo de permanencia (aging) permitido para todas las etapas abiertas del embudo comercial."
    )
    def get(self, request):
        """Return aging config for all open stages, with defaults for unconfigured stages."""
        org = request.profile.org
        configs = {
            c.stage: c
            for c in StageAgingConfig.objects.filter(org=org)
        }

        result = []
        for stage_value, stage_label in STAGES:
            if stage_value in CLOSED_STAGES:
                continue
            if stage_value in configs:
                serializer = StageAgingConfigSerializer(configs[stage_value])
                result.append(serializer.data)
            else:
                result.append({
                    "id": None,
                    "stage": stage_value,
                    "expected_days": DEFAULT_STAGE_EXPECTED_DAYS.get(stage_value, 14),
                    "warning_days": None,
                })
        return Response(result)

    @extend_schema(
        tags=["Opportunity Stages"],
        operation_id="opportunities_stage_aging_bulk_update",
        request=StageAgingConfigSerializer(many=True),
        responses={
            200: inline_serializer(
                name="StageAgingConfigBulkUpdateResponse",
                fields={
                    "error": serializers.BooleanField(),
                    "message": serializers.CharField(),
                    "configs": StageAgingConfigSerializer(many=True)
                }
            ),
            400: inline_serializer(name="StageAgingConfigBadRequest", fields={"error": serializers.BooleanField(), "errors": serializers.CharField()}),
            403: inline_serializer(name="StageAgingConfigForbidden", fields={"error": serializers.BooleanField(), "errors": serializers.CharField()})
        },
        description="Actualiza de forma masiva (bulk upsert) los límites de alerta y días esperados para las etapas del embudo comercial."
    )
    def put(self, request):
        """Bulk upsert stage aging configs (admin only)."""
        if request.profile.role != "ADMIN" and not request.user.is_superuser:
            return Response(
                {"error": True, "errors": "Only admins can update aging config"},
                status=status.HTTP_403_FORBIDDEN,
            )

        org = request.profile.org
        configs_data = request.data
        if not isinstance(configs_data, list):
            return Response(
                {"error": True, "errors": "Expected a list of stage configs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_stages = {s for s, _ in STAGES if s not in CLOSED_STAGES}
        results = []
        for item in configs_data:
            stage = item.get("stage")
            if not stage or stage not in valid_stages:
                continue

            expected_days = item.get("expected_days", 14)
            try:
                expected_days = int(expected_days)
            except (TypeError, ValueError):
                continue
            if expected_days < 1:
                continue

            warning_days = item.get("warning_days")
            if warning_days is not None:
                try:
                    warning_days = int(warning_days)
                except (TypeError, ValueError):
                    warning_days = None

            config, _ = StageAgingConfig.objects.update_or_create(
                org=org,
                stage=stage,
                defaults={
                    "expected_days": expected_days,
                    "warning_days": warning_days,
                },
            )
            results.append(StageAgingConfigSerializer(config).data)

        return Response(
            {"error": False, "message": "Aging config updated", "configs": results},
            status=status.HTTP_200_OK,
        )
