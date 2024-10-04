from rest_framework.views import Response
from rest_framework.serializers import ValidationError
from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


def assert_valid(condition: bool, message: str) -> Response or None:
    """
    Assert conditions
    :param condition: Boolean condition
    :param message: Bad request message
    :return: Response or None
    """
    if not condition:
        raise ValidationError(detail={
            'message': message
        })


class LookupFieldMixin:
    lookup_field = 'workspace_id'

    def filter_queryset(self, queryset):
        if self.lookup_field in self.kwargs:
            lookup_value = self.kwargs[self.lookup_field]
            filter_kwargs = {self.lookup_field: lookup_value}
            queryset = queryset.filter(**filter_kwargs)
        return super().filter_queryset(queryset)


class JSONFieldFilterBackend(BaseFilterBackend):
    """
    Custom filter backend to filter on JSONField for dynamic key lookups.
    Supports filters like detail__{key} and detail__{key}__in.
    """

    def filter_queryset(self, request, queryset, view):
        filters = Q()

        for param, value in request.query_params.items():
            if param.startswith('detail__'):
                filters &= Q(**{param: value if '__in' not in param else value.split(',')})

        return queryset.filter(filters)
