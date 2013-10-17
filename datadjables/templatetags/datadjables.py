from django import template


register = template.Library()


@register.inclusion_tag('datadjables/table_init.html')
def table_init(dtobj):
    """Returns the html code for a DataDjable"""
    return {'dt': dtobj}
