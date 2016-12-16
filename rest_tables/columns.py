from django.forms.utils import flatatt
from django.utils import six
from django.utils.html import format_html

ANGULAR_ROW_VARIABLE = 'row'
DEFAULT_TAG = 'span'

class Column(object):
    type = 'text'
    tag = None

    def __init__(self, angular_exp=None, name=None, ordering=None, filtering=False, attrs=None):
        self.angular_expr = angular_exp
        self.name = name or ''
        self.ordering = ordering
        self.filtering = filtering
        self.attrs = attrs

    def get_angular_expr(self):
        return self.angular_expr or '{}.{}'.format(ANGULAR_ROW_VARIABLE, self.name)

    def get_ordering(self):
        return self.ordering or self.name

    def get_filtering(self):
        return self.filtering if isinstance(self.filtering, six.string_types) else self.name

    def get_attrs(self):
        return self.attrs

    def __call__(self, name=None):
        if name is None:
            return self
        return Column(self.angular_expr, self.name or name, self.ordering, self.filtering, self.attrs)

    def render_angular_expr(self):
        tag = self.tag
        attrs = self.get_attrs()
        value = self.get_angular_expr()
        if attrs and tag is None:
            tag = DEFAULT_TAG
        if not tag:
            return '{{{{ {} }}}}'.format(value)
        return format_html('<{0}{2}>{{{{ {1} }}}}</{0}>', tag, value, flatatt(attrs))