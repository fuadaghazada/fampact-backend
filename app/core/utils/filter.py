from django.db.models import Q
from django_filters import CharFilter, BaseRangeFilter, NumberFilter


class NumberRangeFilter(BaseRangeFilter, NumberFilter):
    pass


class ListFilter(CharFilter):
    """For having OR filter values"""
    def filter(self, queryset, value):
        values = list(filter(lambda x: x != u'', value.split(',')))

        condition = generate_or_conditions(self.field_name, values)

        return queryset.filter(condition)


def generate_or_conditions(field_name, values):
    """Helper method for generating or conditions for filter"""
    condition = Q()
    for data in values:
        condition = condition | Q(**{field_name: data})

    return condition
