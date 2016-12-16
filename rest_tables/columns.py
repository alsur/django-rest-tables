

ANGULAR_ROW_VARIABLE = 'row'


class Column(object):
    def __init__(self, angular_exp=None, name=None, ordering=None):
        self.angular_expr = angular_exp
        self.name = name or ''
        self.ordering = ordering

    def get_angular_expr(self):
        return self.angular_expr or '{}.{}'.format(ANGULAR_ROW_VARIABLE, self.name)

    def get_ordering(self):
        return self.ordering or self.name

    def __call__(self, name=None):
        if name is None:
            return self
        return Column(self.angular_expr, self.name or name, self.ordering)