"""
Public views for client portal.

These views do not require authentication and are accessed via public tokens.
"""

import logging

from django.http import HttpResponse
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

from invoices.models import Invoice, Estimate, InvoiceTemplate
from invoices.pdf import (
    generate_invoice_pdf,
    generate_invoice_filename,
    generate_estimate_pdf,
    generate_estimate_filename,
)

logger = logging.getLogger(__name__)


class PublicInvoiceView(APIView):
    """
    Public view for invoice - accessible via public token.
    No authentication required.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Public Portal"],
        operation_id="public_invoices_retrieve",
        responses={
            200: inline_serializer(
                name="PublicInvoiceResponse",
                fields={
                    "id": serializers.CharField(),
                    "invoice_number": serializers.CharField(),
                    "invoice_title": serializers.CharField(),
                    "status": serializers.CharField(),
                    "client_name": serializers.CharField(),
                    "client_email": serializers.CharField(),
                    "issue_date": serializers.CharField(),
                    "due_date": serializers.CharField(),
                    "subtotal": serializers.CharField(),
                    "discount_amount": serializers.CharField(),
                    "tax_amount": serializers.CharField(),
                    "total_amount": serializers.CharField(),
                    "amount_paid": serializers.CharField(),
                    "amount_due": serializers.CharField(),
                    "currency": serializers.CharField(),
                    "notes": serializers.CharField(allow_blank=True),
                    "terms": serializers.CharField(allow_blank=True),
                    "billing_address": serializers.JSONField(),
                    "line_items": serializers.ListField(child=serializers.JSONField()),
                    "payments": serializers.ListField(child=serializers.JSONField()),
                    "org": serializers.JSONField(),
                    "template": serializers.JSONField()
                }
            ),
            404: inline_serializer(name="PublicInvoiceNotFound", fields={"error": serializers.BooleanField(), "message": serializers.CharField()})
        },
        description="Obtiene los detalles públicos completos de una factura mediante su token único."
    )
    def get(self, request, token):
        """Get invoice by public token"""
        invoice = Invoice.objects.filter(
            public_token=token, public_link_enabled=True
        ).first()

        if not invoice:
            return Response(
                {"error": True, "message": "Invoice not found or link expired"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Track view if first time
        if not invoice.viewed_at:
            invoice.viewed_at = timezone.now()
            if invoice.status == "Sent":
                invoice.status = "Viewed"
            invoice.save()

        # Serialize invoice data for public view
        data = {
            "id": str(invoice.id),
            "invoice_number": invoice.invoice_number,
            "invoice_title": invoice.invoice_title,
            "status": invoice.status,
            "client_name": invoice.client_name,
            "client_email": invoice.client_email,
            "issue_date": invoice.issue_date,
            "due_date": invoice.due_date,
            "subtotal": str(invoice.subtotal),
            "discount_amount": str(invoice.discount_amount),
            "tax_amount": str(invoice.tax_amount),
            "total_amount": str(invoice.total_amount),
            "amount_paid": str(invoice.amount_paid),
            "amount_due": str(invoice.amount_due),
            "currency": invoice.currency,
            "notes": invoice.notes,
            "terms": invoice.terms,
            "billing_address": {
                "line": invoice.billing_address_line,
                "city": invoice.billing_city,
                "state": invoice.billing_state,
                "postcode": invoice.billing_postcode,
                "country": invoice.billing_country,
            },
            "line_items": [
                {
                    "name": item.name or "",
                    "description": item.description,
                    "quantity": str(item.quantity),
                    "unit_price": str(item.unit_price),
                    "total": str(item.total),
                }
                for item in invoice.line_items.all().order_by("order")
            ],
            "payments": [
                {
                    "amount": str(payment.amount),
                    "payment_date": payment.payment_date,
                    "payment_method": payment.payment_method,
                }
                for payment in invoice.payments.all().order_by("-payment_date")
            ],
            "org": {
                "name": invoice.org.name if invoice.org else "",
            },
        }

        # Get default template for styling
        template = invoice.template
        if not template and invoice.org:
            template = InvoiceTemplate.objects.filter(
                org=invoice.org, is_default=True
            ).first()

        if template:
            data["template"] = {
                "primary_color": template.primary_color,
                "secondary_color": template.secondary_color,
                "footer_text": template.footer_text or "",
            }
        else:
            data["template"] = {
                "primary_color": "#3B82F6",
                "secondary_color": "#1E40AF",
                "footer_text": "",
            }

        return Response(data)


class PublicInvoicePDFView(APIView):
    """
    Public PDF download for invoice - accessible via public token.
    No authentication required.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Public Portal"],
        operation_id="public_invoices_pdf",
        responses={
            200: serializers.CharField(), # Flujo plano/stream para descarga binaria de PDF
            404: inline_serializer(name="PublicInvoicePdfNotFound", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            503: inline_serializer(name="PublicInvoicePdfUnavailable", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            500: inline_serializer(name="PublicInvoicePdfError", fields={"error": serializers.BooleanField(), "message": serializers.CharField()})
        },
        description="Descarga el documento binario PDF de la factura mediante su token público sin requerir login."
    )
    def get(self, request, token):
        """Download invoice PDF by public token"""
        invoice = Invoice.objects.filter(
            public_token=token, public_link_enabled=True
        ).first()

        if not invoice:
            return Response(
                {"error": True, "message": "Invoice not found or link expired"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            pdf_content = generate_invoice_pdf(invoice, include_payments=True)
            filename = generate_invoice_filename(invoice)

            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except ImportError:
            logger.exception("PDF generation library not available")
            return Response(
                {"error": True, "message": "PDF generation unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            logger.exception("Failed to generate invoice PDF")
            return Response(
                {"error": True, "message": "Failed to generate PDF"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PublicEstimateView(APIView):
    """
    Public view for estimate - accessible via public token.
    No authentication required.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Public Portal"],
        operation_id="public_estimates_retrieve",
        responses={
            200: inline_serializer(
                name="PublicEstimateResponse",
                fields={
                    "id": serializers.CharField(),
                    "estimate_number": serializers.CharField(),
                    "title": serializers.CharField(),
                    "status": serializers.CharField(),
                    "client_name": serializers.CharField(),
                    "client_email": serializers.CharField(),
                    "issue_date": serializers.CharField(),
                    "expiry_date": serializers.CharField(),
                    "subtotal": serializers.CharField(),
                    "discount_amount": serializers.CharField(),
                    "tax_amount": serializers.CharField(),
                    "total_amount": serializers.CharField(),
                    "currency": serializers.CharField(),
                    "notes": serializers.CharField(allow_blank=True),
                    "terms": serializers.CharField(allow_blank=True),
                    "client_address": serializers.JSONField(),
                    "line_items": serializers.ListField(child=serializers.JSONField()),
                    "org": serializers.JSONField(),
                    "template": serializers.JSONField()
                }
            ),
            404: inline_serializer(name="PublicEstimateNotFound", fields={"error": serializers.BooleanField(), "message": serializers.CharField()})
        },
        description="Obtiene los detalles públicos completos de una cotización mediante su token único."
    )
    def get(self, request, token):
        """Get estimate by public token"""
        estimate = Estimate.objects.filter(
            public_token=token, public_link_enabled=True
        ).first()

        if not estimate:
            return Response(
                {"error": True, "message": "Estimate not found or link expired"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Track view if first time
        if not estimate.viewed_at:
            estimate.viewed_at = timezone.now()
            if estimate.status == "Sent":
                estimate.status = "Viewed"
            estimate.save()

        # Serialize estimate data for public view
        data = {
            "id": str(estimate.id),
            "estimate_number": estimate.estimate_number,
            "title": estimate.title,
            "status": estimate.status,
            "client_name": estimate.client_name,
            "client_email": estimate.client_email,
            "issue_date": estimate.issue_date,
            "expiry_date": estimate.expiry_date,
            "subtotal": str(estimate.subtotal),
            "discount_amount": str(estimate.discount_amount),
            "tax_amount": str(estimate.tax_amount),
            "total_amount": str(estimate.total_amount),
            "currency": estimate.currency,
            "notes": estimate.notes,
            "terms": estimate.terms,
            "client_address": {
                "line": estimate.client_address_line,
                "city": estimate.client_city,
                "state": estimate.client_state,
                "postcode": estimate.client_postcode,
                "country": estimate.client_country,
            },
            "line_items": [
                {
                    "name": item.name or "",
                    "description": item.description,
                    "quantity": str(item.quantity),
                    "unit_price": str(item.unit_price),
                    "total": str(item.total),
                }
                for item in estimate.line_items.all().order_by("order")
            ],
            "org": {
                "name": estimate.org.name if estimate.org else "",
            },
        }

        # Get default template for styling
        if estimate.org:
            template = InvoiceTemplate.objects.filter(
                org=estimate.org, is_default=True
            ).first()
        else:
            template = None

        if template:
            data["template"] = {
                "primary_color": template.primary_color,
                "secondary_color": template.secondary_color,
                "footer_text": template.footer_text or "",
            }
        else:
            data["template"] = {
                "primary_color": "#3B82F6",
                "secondary_color": "#1E40AF",
                "footer_text": "",
            }

        return Response(data)


class PublicEstimatePDFView(APIView):
    """
    Public PDF download for estimate - accessible via public token.
    No authentication required.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Public Portal"],
        operation_id="public_estimates_pdf",
        responses={
            200: serializers.CharField(),
            404: inline_serializer(name="PublicEstimatePdfNotFound", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            503: inline_serializer(name="PublicEstimatePdfUnavailable", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            500: inline_serializer(name="PublicEstimatePdfError", fields={"error": serializers.BooleanField(), "message": serializers.CharField()})
        },
        description="Descarga el documento binario PDF de la cotización mediante su token público."
    )
    def get(self, request, token):
        """Download estimate PDF by public token"""
        estimate = Estimate.objects.filter(
            public_token=token, public_link_enabled=True
        ).first()

        if not estimate:
            return Response(
                {"error": True, "message": "Estimate not found or link expired"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            pdf_content = generate_estimate_pdf(estimate)
            filename = generate_estimate_filename(estimate)

            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except ImportError:
            logger.exception("PDF generation library not available")
            return Response(
                {"error": True, "message": "PDF generation unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            logger.exception("Failed to generate estimate PDF")
            return Response(
                {"error": True, "message": "Failed to generate PDF"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(exclude=True)
class PublicEstimateAcceptView(APIView):
    """
    Public endpoint to accept an estimate - accessible via public token.
    No authentication required.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Public Portal"],
        operation_id="public_estimates_accept",
        responses={
            200: inline_serializer(name="PublicEstimateAcceptSuccess", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            400: inline_serializer(name="PublicEstimateAcceptInvalidState", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            404: inline_serializer(name="PublicEstimateAcceptNotFound", fields={"error": serializers.BooleanField(), "message": serializers.CharField()})
        },
        description="Permite al cliente aceptar la cotización directamente desde el portal público."
    )
    def post(self, request, token):
        """Accept estimate by public token"""
        estimate = Estimate.objects.filter(
            public_token=token, public_link_enabled=True
        ).first()

        if not estimate:
            return Response(
                {"error": True, "message": "Estimate not found or link expired"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if estimate.status not in ["Sent", "Viewed"]:
            return Response(
                {
                    "error": True,
                    "message": "Estimate cannot be accepted in current state",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        estimate.status = "Accepted"
        estimate.accepted_at = timezone.now()
        estimate.save()

        return Response({"error": False, "message": "Estimate accepted successfully"})


@extend_schema(exclude=True)
class PublicEstimateDeclineView(APIView):
    """
    Public endpoint to decline an estimate - accessible via public token.
    No authentication required.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Public Portal"],
        operation_id="public_estimates_decline",
        responses={
            200: inline_serializer(name="PublicEstimateDeclineSuccess", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            400: inline_serializer(name="PublicEstimateDeclineInvalidState", fields={"error": serializers.BooleanField(), "message": serializers.CharField()}),
            404: inline_serializer(name="PublicEstimateDeclineNotFound", fields={"error": serializers.BooleanField(), "message": serializers.CharField()})
        },
        description="Permite al cliente rechazar la cotización desde el portal público."
    )
    def post(self, request, token):
        """Decline estimate by public token"""
        estimate = Estimate.objects.filter(
            public_token=token, public_link_enabled=True
        ).first()

        if not estimate:
            return Response(
                {"error": True, "message": "Estimate not found or link expired"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if estimate.status not in ["Sent", "Viewed"]:
            return Response(
                {
                    "error": True,
                    "message": "Estimate cannot be declined in current state",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        estimate.status = "Declined"
        estimate.declined_at = timezone.now()
        estimate.save()

        return Response({"error": False, "message": "Estimate declined"})
