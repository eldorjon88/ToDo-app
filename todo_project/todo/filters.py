import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    min_priority = django_filters.NumberFilter(field_name="priority", lookup_expr="gte")
    max_priority = django_filters.NumberFilter(field_name="priority", lookup_expr="lte")
    due_before = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")
    due_after = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Task
        fields = ["status", "priority"]
