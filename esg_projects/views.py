import base64

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.template.loader import get_template
from rest_framework.viewsets import ModelViewSet
from xhtml2pdf import pisa
from .models import ESGProject
from .serializers import ESGProjectSerializer


class ESGProjectViewSet(ModelViewSet):
    serializer_class = ESGProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = ESGProject.objects.all()

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True, permission_classes=[AllowAny])
    def generate_report(self, request, pk):
        """
        generates reports
        """
        project = ESGProject.objects.get(pk=pk)

        # Create a PDF report
        template_path = 'pdf_template/reports.html'
        context = {'project': project}
        template = get_template(template_path)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        file_name = f"{project.company_name}_reports.pdf"
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            raise ValueError("Error Generating PDF")

        # Return both the file path and binary content
        content = base64.b64encode(response.getvalue()).decode('utf-8')
        response_data = {"content": content, "name": file_name,
                         "content_type": response.headers.get("Content-Type")}

        response = Response(response_data)
        return response
