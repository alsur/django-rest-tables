from django import template
register = template.Library()

@register.simple_tag
def ngvar(var_name):
    return "{{{{ {} }}}}".format(var_name)


@register.simple_tag
def ngvar_concat(*vars):
    return ngvar(''.join(vars))
