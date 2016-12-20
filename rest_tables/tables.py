from collections import OrderedDict

import six
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from rest_framework.views import get_view_name

from rest_tables.columns import Column


def get_drf_columns(serializer, filter_columns):
    fields = serializer.get_fields()
    return OrderedDict([(name, Column()) for name, column in fields.items() if filter_columns(name, column)])


class DefaultMeta(object):
    view_set = None
    url_name = None
    default_sorting = None
    controller = 'tableController'
    count = None
    columns = None
    exclude = None
    request_params = None

    @classmethod
    def get_default_sorting(cls):
        # TODO: support lists. Use OrderedDict?
        sorting = cls.default_sorting
        if sorting is None:
            return
        is_desc = sorting.startswith('-')
        sorting = sorting[1:] if is_desc else sorting
        return {sorting: 'desc' if is_desc else 'asc'}

    @classmethod
    def get_initial_params(cls):
        initial_params = {
            'count': cls.count,
            'counts': [],
            'sorting': cls.get_default_sorting(),
        }
        return {key: value for key, value in initial_params.items() if value is not None}

    @classmethod
    def get_url(cls):
        url_name = cls.url_name
        if not url_name:
            url_name = get_view_name(cls.view_set).lower()
            url_name = '{}-list'.format(url_name)
        return reverse(url_name)


def create_meta(meta_class=None):
    if meta_class is None or meta_class is DefaultMeta:
        class Meta(DefaultMeta):
            pass
        return Meta
    class Meta(meta_class, DefaultMeta):
        pass
    return Meta


class MetaTable(type):
    @classmethod
    def __prepare__(mcs, name, bases):
         return OrderedDict()

    def __new__(cls, name, bases, attrs, **kwargs):
        table = super(MetaTable, cls).__new__(cls, name, bases, attrs, **kwargs)
        table.__columns__ = cls.get_columns(attrs)
        table.Meta = create_meta(attrs.get('Meta'))
        return table

    @classmethod
    def get_columns(cls, attrs=None):
        attrs = attrs or {key: getattr(cls, key) for key in dir(cls)}
        return OrderedDict([(key, column) for key, column in attrs.items() if isinstance(column, Column)])


class Table(six.with_metaclass(MetaTable)):
    def __init__(self, request_params=None):
        self.drf_serializer = self.Meta.view_set.serializer_class()
        self.columns = self.get_columns()
        self.request_params = dict(self.Meta.request_params or {}, **request_params or {})

    def get_columns(self):
        columns = self.get_default_columns()
        columns.update(self.__columns__)
        return columns

    def _filter_column(self, name, column):
        if name in (self.Meta.exclude or ()):
            return False
        if not self.Meta.columns or name in self.Meta.columns:
            return True

    def get_default_columns(self):
        return get_drf_columns(self.drf_serializer, self._filter_column)

    def get_columns_order(self):
        if not self.Meta.columns:
            return
        def columns_order(item):
            column_name = item[0]
            if not column_name in self.Meta.columns:
                # Move at the end
                return 99999
            return self.Meta.columns.index(column_name)
        return columns_order

    def render_columns(self):
        columns = self.columns.items()
        order = self.get_columns_order()
        if order:
            columns = sorted(columns, key=order)
        return [column(name) for name, column in columns]

    def as_html(self):
        template = get_template('rest_tables/table.html')
        context = {
            'table': self,
            'controller': self.Meta.controller,
            'initial_params': self.Meta.get_initial_params,
            'url': self.Meta.get_url(),
            'url_params': self.request_params,
        }
        return template.render(context)

    Meta = DefaultMeta
