from collections import OrderedDict

import six
from django.core.urlresolvers import reverse
from django.template.loader import get_template

from rest_tables.columns import Column


class DefaultMeta(object):
    url_name = None
    default_sorting = None
    controller = 'tableController'
    count = None

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
        return reverse(cls.url_name)


def create_meta(meta_class=None):
    if meta_class is None:
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
    def __init__(self):
        self.columns = self.get_columns()
        pass

    def get_columns(self):
        return self.__columns__

    def render_columns(self):
        columns = self.columns
        return [column(name) for name, column in columns.items()]

    def as_html(self):
        template = get_template('rest_tables/table.html')
        context = {
            'table': self,
            'controller': self.Meta.controller,
            'initial_params': self.Meta.get_initial_params,
            'url': self.Meta.get_url()
        }
        return template.render(context)
