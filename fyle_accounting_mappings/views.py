import logging
from typing import Dict, List

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import status
from django.db.models import Count

from .exceptions import BulkError
from .utils import assert_valid
from .models import MappingSetting, Mapping, ExpenseAttribute, DestinationAttribute, EmployeeMapping, CategoryMapping
from .serializers import MappingSettingSerializer, MappingSerializer, \
    EmployeeMappingSerializer, CategoryMappingSerializer

logger = logging.getLogger(__name__)


class MappingSettingsView(ListCreateAPIView):
    """
    Mapping Settings VIew
    """
    serializer_class = MappingSettingSerializer

    def get_queryset(self):
        return MappingSetting.objects.filter(workspace_id=self.kwargs['workspace_id'])

    def post(self, request, *args, **kwargs):
        """
        Post mapping settings
        """
        try:
            mapping_settings: List[Dict] = request.data

            assert_valid(mapping_settings != [], 'Mapping settings not found')

            mapping_settings = MappingSetting.bulk_upsert_mapping_setting(mapping_settings, self.kwargs['workspace_id'])

            return Response(data=self.serializer_class(mapping_settings, many=True).data, status=status.HTTP_200_OK)
        except BulkError as exception:
            logger.error(exception.response)
            return Response(
                data=exception.response,
                status=status.HTTP_400_BAD_REQUEST
            )


class MappingsView(ListCreateAPIView):
    """
    Mapping Settings VIew
    """
    serializer_class = MappingSerializer

    def get_queryset(self):
        source_type = self.request.query_params.get('source_type')

        assert_valid(source_type is not None, 'query param source type not found')

        if int(self.request.query_params.get('table_dimension')) == 3:
            mappings = Mapping.objects.filter(source_id__in=Mapping.objects.filter(
                source_type=source_type, workspace_id=self.kwargs['workspace_id']).values('source_id').annotate(
                    count=Count('source_id')).filter(count=2).values_list('source_id'))
        else:
            mappings = Mapping.objects.filter(source_type=source_type, workspace_id=self.kwargs['workspace_id'])

        return mappings.order_by('source__value')

    def post(self, request, *args, **kwargs):
        """
        Post mapping settings
        """
        source_type = request.data.get('source_type', None)

        assert_valid(source_type is not None, 'source type not found')

        destination_type = request.data.get('destination_type', None)

        assert_valid(destination_type is not None, 'destination type not found')

        source_value = request.data.get('source_value', None)

        destination_value = request.data.get('destination_value', None)

        destination_id = request.data.get('destination_id', None)

        assert_valid(destination_value is not None, 'destination value not found')
        try:
            mappings = Mapping.create_or_update_mapping(
                source_type=source_type,
                destination_type=destination_type,
                source_value=source_value,
                destination_value=destination_value,
                destination_id=destination_id,
                workspace_id=self.kwargs['workspace_id']
            )

            return Response(data=self.serializer_class(mappings).data, status=status.HTTP_200_OK)
        except ExpenseAttribute.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Fyle {0} with name {1} does not exist'.format(source_type, source_value)
                }
            )
        except DestinationAttribute.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Destination {0} with name {1} does not exist'.format(
                        destination_type, destination_value)
                }
            )


class EmployeeMappingsView(ListCreateAPIView):
    """
    Employee Mappings View
    """
    serializer_class = EmployeeMappingSerializer

    def get_queryset(self):
        return EmployeeMapping.objects.filter(
            workspace_id=self.kwargs['workspace_id']
        ).all().order_by('source_employee__value')


class CategoryMappingsView(ListCreateAPIView):
    """
    Category Mappings View
    """
    serializer_class = CategoryMappingSerializer

    def get_queryset(self):
        return CategoryMapping.objects.filter(
            workspace_id=self.kwargs['workspace_id']
        ).all().order_by('source_category__value')
