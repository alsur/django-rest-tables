from django.template.loader_tags import register


@register.simple_tag
def rest_table(table, name=None):
    """
    Displays the row of buttons for delete and save.
    """
    return table.as_html()
