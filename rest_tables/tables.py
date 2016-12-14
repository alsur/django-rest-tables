import six
from django.template.loader import get_template

from rest_tables.columns import Column


class MetaTable(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        return super(MetaTable, cls).__new__(cls, name, bases, attrs, **kwargs)

    def get_columns(cls, attrs):
        return {key: column for key, column in attrs.items() if isinstance(column, Column)}


class Table(six.with_metaclass(MetaTable)):

    def as_html(self):
        template = get_template('rest_tables/table.html')
        context = {
            'table': self,
        }
        return template.render(context)
