import django_filters
from .models import Post
from django import forms


class PostFilter(django_filters.FilterSet):
    title_post = django_filters.CharFilter(lookup_expr='icontains')
    author__name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    date_time_post__gt = django_filters.DateTimeFilter(field_name='date_time_post', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title_post', 'author__name', 'date_time_post__gt']
