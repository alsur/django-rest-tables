from collections import OrderedDict

import six
from django.template.loader import get_template

from rest_tables.columns import Column


class MetaTable(type):
    @classmethod
    def __prepare__(mcs, name, bases):
         return OrderedDict()

    def __new__(cls, name, bases, attrs, **kwargs):
        table = super(MetaTable, cls).__new__(cls, name, bases, attrs, **kwargs)
        table.__columns__ = cls.get_columns(attrs)
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
        }
        return template.render(context)
